import os
import sys

sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

import torch
from transformers import BertForQuestionAnswering, BertTokenizer
from wordembedding.utils import split_sentence
from basefunction import json2list

from QA.infer import evaluate



def load_qa_model(model_path= 'NLP/QA/models'):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    model_class = BertForQuestionAnswering
    model = model_class.from_pretrained(model_path)
    model.to(device)

    tokenizer_class = BertTokenizer
    tokenizer = tokenizer_class.from_pretrained(model_path, do_lower_case=False, cache_dir=None)

    return model, tokenizer


def QA_system(model, tokenizer, question, json_script):
    context = split_sentence(json_script)

    answers = evaluate(model, tokenizer, question, context)

    result = list()
    prev_idx = None
    for answer in answers:
        for i, script in enumerate(json_script):
            if answer in script['text']:
                if i == prev_idx:
                    continue
                result.append(script)
                prev_idx = i

    return result
