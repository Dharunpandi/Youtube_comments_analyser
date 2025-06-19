from flask import Flask, render_template, request
from processing import run_comment_analysis
from comment_extraction import extract_comments
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        video_id = request.form['video_id'].strip()
        comments_json_path = extract_comments(video_id)

        if not comments_json_path or not os.path.exists(comments_json_path):
            return render_template("home.html", error="Could not extract comments. Please check the video ID.")

        analysis = run_comment_analysis(comments_json_path)

        if isinstance(analysis, str) and "error" in analysis.lower():
            return render_template("home.html", error="Analysis failed: " + analysis)

        creator_name = analysis.get("creator_name", "Creator")
        sections = analysis.get("sections", {})

        sentiment_counts = analysis.get("sentiment_analysis", {}).get("sentiment_counts", {})
        sentiment_percentages = analysis.get("sentiment_analysis", {}).get("sentiment_percentages", {})

        return render_template("results.html",
                               creator_name=creator_name,
                               sections=sections,
                               sentiment_counts=sentiment_counts,
                               sentiment_percentages=sentiment_percentages)

    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)
