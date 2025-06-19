import os
import pandas as pd
import google.generativeai as genai
import re
import json

api_key = os.getenv("GENAI_API_KEY", 'AIzaSyBvLns6edyYX3Ak0ceoFSKph-AKgWW6bAk')
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.7,
    "max_output_tokens": 30000,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    generation_config=generation_config
)

def get_sentiment_breakdown(comment_block):
    prompt = f"""
You are a sentiment classifier. Given a list of comments, classify them as Positive, Neutral, or Negative. 

Return counts in this format:
Positive: X
Neutral: X
Negative: X

Here are the comments:
{comment_block}
"""
    result = model.generate_content(prompt).text.strip()
    matches = re.findall(r'(Positive|Neutral|Negative):\s*(\d+)', result)
    counts = {label.lower(): int(count) for label, count in matches}

    total = sum(counts.values()) if counts else 1
    percentages = {k: round((v / total) * 100, 2) for k, v in counts.items()}

    return {
        "sentiment_counts": counts,
        "sentiment_percentages": percentages
    }

def parse_response_to_json(response, creator_name):
    sections = {}
    current_section = None
    current_text = ""
    score_pattern = re.compile(r"Score:\s*([0-9.]+)/10")

    for line in response.splitlines():
        line = line.strip()
        if line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4.") or line.startswith("5.") or line.startswith("6."):
            if current_section and current_text:
                score_match = score_pattern.search(current_text)
                score = float(score_match.group(1)) if score_match else 0
                sections[current_section] = {
                    "feedback": current_text.strip(),
                    "score": score
                }
            current_section = re.sub(r"\d+\.\s*", "", line)
            current_text = ""
        else:
            current_text += line + "\n"

    if current_section and current_text:
        score_match = score_pattern.search(current_text)
        score = float(score_match.group(1)) if score_match else 0
        sections[current_section] = {
            "feedback": current_text.strip(),
            "score": score
        }

    return {
        "creator_name": creator_name,
        "sections": sections
    }

def run_comment_analysis(json_file_path, output_file_path="youtube_analysis_result.json"):
    try:
        df = pd.read_json(json_file_path)
        creator_name = df['creator'].dropna().unique()
        creator_name = creator_name[0] if len(creator_name) > 0 else "the creator"

        comment_list = df['text'].dropna().tolist()
        if not comment_list:
            return {"error": "No comments available for analysis"}

        comment_block = "\n".join([f"- {comment}" for comment in comment_list])
        sentiment_result = get_sentiment_breakdown(comment_block)

        # Prompt for Gemini
        prompt = f"""
You are an expert YouTube comment analyst. Below is a list of real YouTube comments for a specific video. Your task is to analyze these comments and return a structured report directly to the video creator.

Here is the creator's name:
{creator_name}

Here are the user comments:
{comment_block}

Now return the analysis using this format:

Hi {creator_name}, I'm your YouTube analysis assistant helping you understand how viewers reacted to your video.

1. Content Appreciation
[Points]
Score: X/10

2. Suggestions for Improvement
[Points]
Score: X/10

3. Criticism
[Points]
Score: X/10

4. Spam or Trolling
[Points]
Score: X/10

5. Technical Issues
[Points]
Score: X/10

6. Overall Video Score
[One line summary]
Score: X/10
"""
        response = model.generate_content(prompt).text.strip()
        result_json = parse_response_to_json(response, creator_name)

        final_output = {
            "creator_name": result_json["creator_name"],
            "sections": result_json["sections"],
            "sentiment_analysis": sentiment_result
        }

        with open(output_file_path, "w") as f:
            json.dump(final_output, f, indent=2)

        return final_output

    except Exception as e:
        return {"error": str(e)}
