# !pip install youtube_transcript_api
#!pip install - r requirements.txt
from bson import ObjectId
#from youtube_transcript_api.formatters import JSONFormatter
#from youtube_transcript_api import YouTubeTranscriptApi
import xmltodict
from pytube import YouTube
import sys
import json
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


def download_script(id):
  video_id = id
  yt = YouTube('https://youtube.com/watch?v='+str(video_id))
  
  code = ''
  for c in yt.captions:
    if 'ko' in c.code:
      code = c.code
      break
  scriptions = xmltodict.parse(
    yt.captions.get_by_language_code(code).xml_captions)
  
  scriptions = json.loads(json.dumps(scriptions))
  scriptions = scriptions['transcript']['text']
  result = []
  for sc in scriptions:
    result.append({
        'start': sc['@start'],
        'text': sc['#text']
    })

  title = yt.title

  script_result = {
    'video_id': video_id,
    'title': title,
    'scriptions': result,
    'summarization': '',
  }

  return script_result#json.dumps(data_transcript, ensure_ascii=False)
