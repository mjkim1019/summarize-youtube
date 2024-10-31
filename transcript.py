import os

import requests
import re
from youtube_transcript_api import YouTubeTranscriptApi

# YouTube API 설정
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/videos"

def extract_video_id(url):
    # URL에서 v= 또는 /shorts/ 뒤의 ID 추출
    match = re.search(r"(?:v=|/shorts/)([a-zA-Z0-9_-]+)", url)
    return match.group(1) if match else None

def get_video_info(video_id):
    """YouTube 동영상 제목, 채널 이름, 썸네일 URL, 조회수를 가져오는 함수"""
    params = {
        "part": "snippet,statistics",
        "id": video_id,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(YOUTUBE_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["items"]:
            item = data["items"][0]
            video_info = {
                "title": item["snippet"]["title"],
                "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
                "channel_title": item["snippet"]["channelTitle"],
                "view_count": item["statistics"]["viewCount"]
            }
            return video_info
    return None

def get_video_captions(url):
    try:
        video_id = url.replace('https://www.youtube.com/watch?v=', '')
        print(">> video_id = " + video_id)

        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        print(transcript)

        output = ''
        for x in transcript:
            sentence = x['text']
            output += f' {sentence}\n'

        print(output)
        return output
    except Exception as e:
        return "No captions available"


def main():
    url = 'https://www.youtube.com/watch?v=1SizhsIcqEY'

    # 사용자가 동영상 ID를 입력
    video_url = input("Enter the YouTube video URL: ")
    video_id = extract_video_id(video_url)

    # 동영상 정보 가져오기
    video_info = get_video_info(video_id)
    if video_info:
        print("Title:", video_info["title"])
        print("Channel:", video_info["channel_title"])
        print("Thumbnail URL:", video_info["thumbnail"])
        print("View Count:", video_info["view_count"])
    else:
        print("Could not retrieve video information.")

    # 자막 가져오기
    captions = get_video_captions(video_id)
    print("Captions:", captions)

# 프로그램의 시작점
if __name__ == "__main__":
    main()