from youtube_transcript_api import YouTubeTranscriptApi

video_id = "E0Hmnixke2g"

api = YouTubeTranscriptApi()

transcript_list = api.list(video_id)

print("Available transcripts:\n")

for transcript in transcript_list:
    print(
        f"Language: {transcript.language} "
        f"| Code: {transcript.language_code} "
        f"| Generated: {transcript.is_generated}"
    )