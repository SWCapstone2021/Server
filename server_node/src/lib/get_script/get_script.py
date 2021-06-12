#from youtube_transcript_api.formatters import JSONFormatter
#from youtube_transcript_api import YouTubeTranscriptApi
import xmltodict
# from six.moves import html_parser
# html = html_parser.HTMLParser()
from pytube import YouTube
import sys
import json
import io
#sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
#sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
# sys.stdout.reconfigure(encoding='utf-8')


# def get_script(id):
    
#     video_id = [id]

    
#     transcript = YouTubeTranscriptApi.get_transcripts(
#         video_id, languages=['ko'])

    
#     transcript = transcript[0]
#     sub = transcript[id]
#     for x in sub:
#         x.pop('duration', None)

    
#     data_transcript = {
#         "video_id": id,
#         "transcript": sub,
#     }

#     print(json.dumps(data_transcript, ensure_ascii=False))
    
def get_script(id):
   
  video_id = id
  yt = YouTube('https://youtube.com/watch?v='+str(video_id))
  #raise Exception(yt.captions)
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
    'transcript': result
  }

  print(json.dumps(script_result, ensure_ascii=False))


def main():
    get_script(sys.argv[1])


main()
