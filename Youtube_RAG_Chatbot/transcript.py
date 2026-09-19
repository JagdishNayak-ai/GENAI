from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)


def get_transcript(video_id):
    try:
        api = YouTubeTranscriptApi()

        transcript_list = api.fetch(
            video_id,
            languages=["en"]
        )

        transcript = " ".join(
            snippet.text for snippet in transcript_list
        )

        return transcript

    except TranscriptsDisabled:
        raise Exception(
            "Transcripts are disabled for this YouTube video."
        )

    except NoTranscriptFound:
        raise Exception(
            "No English transcript was found for this video."
        )

    except VideoUnavailable:
        raise Exception(
            "This YouTube video is unavailable or cannot be accessed."
        )

    except Exception as e:
        raise Exception(
            f"Could not retrieve the transcript: {str(e)}"
        )