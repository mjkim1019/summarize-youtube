from youtube_transcript_api import YouTubeTranscriptApi

url = 'https://www.youtube.com/watch?v=1SizhsIcqEY'
#url = 'https://www.youtube.com/watch?v=2TL3DgIMY1g'
print(">> youtube_url = " + url)

video_id = url.replace('https://www.youtube.com/watch?v=', '')
print(">> video_id = " + video_id)

transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
print(transcript)

output = ''
for x in transcript:
    sentence = x['text']
    output += f' {sentence}\n'

print(output)