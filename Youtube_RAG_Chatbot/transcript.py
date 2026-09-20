import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.freetranscriptapi.com/v1/transcript"


def get_transcript(video_id):
    try:
        api_key = os.getenv("TRANSCRIPT_API_KEY")

        if not api_key:
            raise Exception(
                "TRANSCRIPT_API_KEY is missing from .env"
            )

        response = requests.get(
            API_URL,
            params={
                "video_url": video_id,
                "lang": "en"
            },
            headers={
                "Authorization": f"Bearer {api_key}"
            },
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        transcript_lines = data.get("transcript", [])

        if not transcript_lines:
            raise Exception(
                "No transcript was found for this video."
            )

        transcript = " ".join(
            item["text"]
            for item in transcript_lines
        )

        return transcript

    except requests.exceptions.HTTPError as e:
        try:
            error_data = response.json()
            message = error_data.get("error", {}).get(
                "message",
                str(e)
            )
        except Exception:
            message = str(e)

        raise Exception(
            f"Transcript API error: {message}"
        )

    except requests.exceptions.RequestException as e:
        raise Exception(
            f"Transcript API request failed: {str(e)}"
        )

    except Exception as e:
        raise Exception(
            f"Could not retrieve the transcript: {str(e)}"
        )