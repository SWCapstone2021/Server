# Copyright (c) 2020, Soohwan Kim. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sys
from glob import glob

import numpy as np
import torch
import torch.nn as nn
import torchaudio
from torch import Tensor

sys.path.append((os.path.dirname(__file__)))

from kospeech.vocabs.ksponspeech import KsponSpeechVocabulary
from kospeech.audio.core import load_audio
from kospeech.models import (
    ListenAttendSpell,
)


def parse_audio_separate(audio_path: str, del_silence: bool = False, audio_extension: str = 'pcm'):
    paths = sorted(glob(os.path.join(audio_path, '*.wav')), key=lambda i: int(os.path.basename(i)[:-4]))
    features = list()
    input_lengths = list()

    for path in paths:
        signal = load_audio(path, del_silence, extension=audio_extension)
        feature = torchaudio.compliance.kaldi.fbank(
            waveform=Tensor(signal).unsqueeze(0),
            num_mel_bins=80,
            frame_length=20,
            frame_shift=10,
            window_type='hamming'
        ).transpose(0, 1).numpy()

        feature -= feature.mean()
        feature /= np.std(feature)
        feature = torch.FloatTensor(feature).transpose(0, 1)

        features.append(feature)
        input_lengths.append(torch.LongTensor([len(feature)]))

    return features, input_lengths


def parse_audio(audio_path: str, del_silence: bool = False, audio_extension: str = 'pcm'):
    signals, time_stamps = load_audio(audio_path, del_silence, extension=audio_extension)
    features = list()
    input_lengths = list()

    for signal in signals:
        feature = torchaudio.compliance.kaldi.fbank(
            waveform=Tensor(signal).unsqueeze(0),
            num_mel_bins=80,
            frame_length=20,
            frame_shift=10,
            window_type='hamming'
        ).transpose(0, 1).numpy()

        feature -= feature.mean()
        feature /= np.std(feature)

        feature = torch.FloatTensor(feature).transpose(0, 1)

        features.append(feature)
        input_lengths.append(torch.LongTensor([len(feature)]))

    return features, input_lengths, time_stamps


def stt(model, vocab, audio_path):
    features, input_lengths, time_stamps = parse_audio(audio_path, del_silence=True, audio_extension='wav')
    sentences = list()

    for feature, input_length, time_stamp in zip(features, input_lengths, time_stamps):
        y_hats = model.recognize(feature.unsqueeze(0).to('cuda'), input_length)
        sentence = vocab.label_to_string(y_hats.cpu().detach().numpy())
        sentences.append((time_stamp, sentence[0]))

    return sentences


def load_model(model_name='ds2'):
    device = 'cuda'

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
