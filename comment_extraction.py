import googleapiclient.discovery
import pandas as pd
import re
from urllib.parse import urlparse, parse_qs

# YouTube API setup
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyC1v15Lpl4-mnQZHcUfHBoqS5r6VgHyiR0"  # Replace with your YouTube API key

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY
)

def extract_video_id(url):
    """
    Extracts the video ID from a YouTube URL.
    Supports full URLs, shortened URLs, and embed links.
    """
    try:
        parsed_url = urlparse(url)

        if "youtube" in parsed_url.netloc:
            # For standard URLs like https://www.youtube.com/watch?v=VIDEO_ID
            query = parse_qs(parsed_url.query)
            return query.get("v", [None])[0]
        elif "youtu.be" in parsed_url.netloc:
            # For shortened URLs like https://youtu.be/VIDEO_ID
            return parsed_url.path.lstrip('/')
        else:
            return None
    except Exception as e:
        print(f"❌ Failed to parse video ID: {e}")
        return None

def get_video_creator(video_id):
    try:
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()

        if response['items']:
            return response['items'][0]['snippet']['channelTitle']
        else:
            return "Unknown Creator"
    except Exception as e:
        return f"Error fetching creator: {str(e)}"

def extract_comments(video_url: str, output_path: str = "youtube_comments.json"):
    try:
        video_id = extract_video_id(video_url)
        if not video_id:
            print("❌ Invalid YouTube URL")
            return None

        creator_name = get_video_creator(video_id)
        print(f"The content creator's name is: {creator_name}")

        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100
        )
        response = request.execute()

        comments = []
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([
                creator_name,
                comment['authorDisplayName'],
                comment['publishedAt'],
                comment['updatedAt'],
                comment['likeCount'],
                comment['textDisplay']
            ])

        df = pd.DataFrame(comments, columns=[
            'creator', 'author', 'published_at', 'updated_at', 'like_count', 'text'
        ])

        df.to_json(output_path, orient='records', indent=2)
        print(f"\n✅ Comments saved to {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Failed to extract comments: {str(e)}")
        return None
