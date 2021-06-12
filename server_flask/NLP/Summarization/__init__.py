import sys, os
sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from pororo import Pororo


def load_summ_model():
    model = Pororo(task="text_summarization", lang="ko", model="extractive")
    return model
