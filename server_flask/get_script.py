# !pip install youtube_transcript_api
#!pip install - r requirements.txt
from bson import ObjectId
from youtube_transcript_api.formatters import JSONFormatter
from youtube_transcript_api import YouTubeTranscriptApi
import sys
import json
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


def download_script(id):
    # id
    video_id = [id]

    #
    transcript = YouTubeTranscriptApi.get_transcripts(
        video_id, languages=['ko'])

    #
    transcript = transcript[0]
    sub = transcript[id]
    for x in sub:
        x.pop('duration', None)

    #
    data_transcript = {
        "video_id": id,
        "transcript": sub,
        "summarization": ''
    }

    return data_transcript#json.dumps(data_transcript, ensure_ascii=False)
