from youtube_transcript_api.formatters import JSONFormatter
from youtube_transcript_api import YouTubeTranscriptApi
import sys
import json
import io
#sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
#sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
# sys.stdout.reconfigure(encoding='utf-8')


# import subprocess
# import sys


# def install(package):
#     subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# package_list = ["youtube_transcript_api", "requirements.txt"]
# install(package_list)


# !pip install youtube_transcript_api
# !pip install - r requirements.txt


def get_script(id):
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
    }

    print(json.dumps(data_transcript, ensure_ascii=False))
    # return data_transcript


def main():
    get_script(sys.argv[1])


main()
