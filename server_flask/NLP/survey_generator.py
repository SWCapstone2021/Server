import json
import os
import time
import urllib
from urllib.parse import urlparse

from youtube_transcript_api import YouTubeTranscriptApi

from QA import load_qa_model, QA_system
from Summarization import load_summ_model
from wordembedding import *

os.environ["CUDA_VISIBLE_DEVICES"] = "2"


class Example:
    def __init__(self, id, questions):
        self.id = id
        self.questions = questions
        self.answers = list()
        self.score = 0
        self.summary = ''
        self.script = self.load_script()
        self.title, self.author = self.load_title()

    def load_script(self):
        file_path = f"survey_script/{id}.json"
        if not os.path.exists(file_path):
            script = self.download_script()
            return script

        with open(file_path, 'r') as f:
            script = json.load(f)

        return script

    def download_script(self):
        transcript = YouTubeTranscriptApi.get_transcripts([self.id], languages=['ko'])

        transcript = transcript[0]
        sub = transcript[self.id]
        for x in sub:
            x.pop('duration', None)

        return sub

    def load_title(self):
        params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % self.id}
        url = "https://www.youtube.com/oembed"
        query_string = urllib.parse.urlencode(params)
        url = url + "?" + query_string

        with urllib.request.urlopen(url) as response:
            response_text = response.read()
            data = json.loads(response_text.decode())

        return [data['title'], data['author_name']]

    def __str__(self):
        return f"author: {self.author}\ntitle: {self.title}\nsub: {self.script}\nquestion: {self.questions}"


def load_models():
    wm_model = load_wm_model()
    qa_model, qa_tokenizer = load_qa_model()
    summ_model = load_summ_model()
    sc_model = load_sc_model()

    return [wm_model, qa_model, qa_tokenizer, summ_model, sc_model]


if __name__ == "__main__":
    wm_model, qa_model, qa_tokenizer, summ_model, sc_model = load_models()

    ids = ['R_Llt7SnSFA', 'bGBfCrQgZd0', '3snbJdQmTwA', 'c7tEAx2TL2k', 'J9CF-vj5GZU', '4puc2Ox9_vc']

    questions = [
        ['성능이 얼마나 개선되었나?', '펜슬 호환성은 좋은가?'],
        ['등과 땅이 모두 붙어야 하나요?', 'leg raise를 하면 허리가 아플 수 있나요?'],
        ['사건이 일어난 날짜는?', '마스크를 안쓴 사람은?'],
        ['지네딘 지단이 나오는 영화는?', '킹 아서: 제왕의 검에 출연하는 선수는?'],
        ['오케스트라 입장객 수는?', '세중문화회관 개관 날짜는?'],
        ['얀센 백신의 장점은?', '얀센 백신은 몇 명분?']
    ]

    examples = list(map(lambda x, y: Example(x, y), ids, questions))

    start = time.time()
    for e in examples:
        e.score = cosin_similar(e.title, e.script, sc_model)
        e.summary = summary_script(e.script, summ_model)

        for q in e.questions:
            answer = QA_system(qa_model, qa_tokenizer, q, e.script)
            e.answers.append(answer)

    print(f"running time: {time.time() - start}")

    for e in examples:
        print('=' * 10)
        print(f'https://www.youtube.com/watch?v={e.id}')
        print(e.title)
        print(e.score)
        print('summary: ', e.summary)
        print(e.questions[0])
        print(list(map(lambda x: x['text'], e.answers[0])))
        print(e.questions[1])
        print(list(map(lambda x: x['text'], e.answers[1])))
