import os

from youtube_transcript_api import YouTubeTranscriptApi

from QA import load_qa_model, QA_system
from STT import load_stt_model, stt
from Summarization import load_summ_model
from wordembedding import *

# from pprint import pprint as pp


os.environ["CUDA_VISIBLE_DEVICES"] = "2"


def download_script(id):
    transcript = YouTubeTranscriptApi.get_transcripts([id], languages=['ko'])

    transcript = transcript[0]
    sub = transcript[id]
    for x in sub:
        x.pop('duration', None)

    return sub


if __name__ == "__main__":
    i = input("fucntion num:  1(ctrl+F), 2(reliability), 3(STT), 4(association), 5(summarization), 6(QA)")

    json_file = download_script('R_Llt7SnSFA')

    if i == '1':
        SearchingValue = input("keyword:")
        result_script = ctrl_f(SearchingValue, json_file)
        # pp(result_script[:5])

    if i == '2':
        sc_model = load_sc_model()
        SearchingValue = input("keyword:")
        score = cosin_similar(SearchingValue, json_file, sc_model)
        # print(score)

    if i == '3':
        print("Load model...", end='')
        stt_model, stt_vocab = load_stt_model()
        print("done")

        audio_path = 'data/origin_audio/2YD2p24EKb4.wav'

        sentences = stt(stt_model, stt_vocab, audio_path)
        # pp(sentences[:5])

    if i == '4':
        wm_model = load_wm_model()
        SearchingValue = input("keyword:")
        result_script = association_f(SearchingValue, json_file, wm_model)
        # pp(result_script)

    if i == '5':
        summ_model = load_summ_model()
        summ_script = summary_script(json_file, summ_model)
        # pp(summ_script)

    if i == '6':
        print("Load model...", end='')
        qa_model, qa_tokenizer = load_qa_model()
        print("done")

        question = '이혼한 날'
        answers = QA_system(qa_model, qa_tokenizer, question, json_file)
        # pp(answers[:5)
