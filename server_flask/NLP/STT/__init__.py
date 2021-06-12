import os
import sys

import torch
import torch.nn as nn

sys.path.append((os.path.dirname(__file__)))
#sys.path.append((os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

from pre_processing import parse_audio
from kospeech.vocabs.ksponspeech import KsponSpeechVocabulary
from kospeech.models import (
    ListenAttendSpell,
)


def to_json(sentences):
    result = list()
    for sentence in sentences:
        _dict = {
            "id": 0,
            "time": sentence[0],
            "text": sentence[1]
        }
        result.append(_dict)
    return result


def stt(model, vocab, audio_path):
    features, input_lengths, time_stamps = parse_audio(audio_path)
    sentences = list()

    for feature, input_length, time_stamp in zip(features, input_lengths, time_stamps):
        y_hats = model.recognize(feature.unsqueeze(0).to('cuda'), input_length)
        sentence = vocab.label_to_string(y_hats.cpu().detach().numpy())
        sentences.append((time_stamp, sentence[0]))

    return to_json(sentences)


def load_stt_model(model_name='ds2'):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    model = torch.load(os.path.join('STT/models', f"{model_name}.pt"), map_location=lambda storage, loc: storage).to(
        device)
    if isinstance(model, nn.DataParallel):
        model = model.module
    model.eval()

    if isinstance(model, ListenAttendSpell):
        model.encoder.device = device
        model.decoder.device = device

    vocab = KsponSpeechVocabulary('STT/kospeech/aihub_character_vocabs.csv')

    return model, vocab
