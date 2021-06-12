"""
Copyright 2019-present NAVER Corp.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
     http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# -*- coding: utf-8 -*-
import os
import sys
import json
import math
import random
import argparse
import numpy as np
from tqdm import tqdm
from wcwidth import wcswidth
from glob import glob

import torch
import torch.nn as nn

import Levenshtein as Lev

import label_loader
from data_loader import AudioDataLoader, SpectrogramDataset

from models import EncoderRNN, DecoderRNN, Seq2Seq

os.chdir(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

char2index = dict()
index2char = dict()
SOS_token = 0
EOS_token = 0
PAD_token = 0


def fmt(x, w, align='l'):
    x = str(x)
    l = wcswidth(x)
    s = w - l
    if s <= 0:
        return x
    elif align == 'l':
        return x + ' ' * s
    elif align == 'c':
        sl = s // 2
        sr = s - sl
        return ' ' * sl + x + ' ' * sr
    return ' ' * s + x


def label_to_string(labels):
    if len(labels.shape) == 1:
        sent = str()
        for i in labels:
            if i.item() == EOS_token:
                break
            sent += index2char[i.item()]
        return sent

    elif len(labels.shape) == 2:
        sents = list()
        for i in labels:
            sent = str()
            for j in i:
                if j.item() == EOS_token:
                    break
                sent += index2char[j.item()]
            sents.append(sent)

        return sents


def char_distance(ref, hyp):
    ref = ref.replace(' ', '')
    hyp = hyp.replace(' ', '')

    dist = Lev.distance(hyp, ref)
    length = len(ref.replace(' ', ''))

    return dist, length


def get_distance(ref_labels, hyp_labels):
    total_dist = 0
    total_length = 0
    transcripts = []
    for i in range(len(ref_labels)):
        ref = label_to_string(ref_labels[i])
        hyp = label_to_string(hyp_labels[i])

        transcripts.append(f'{fmt(ref, 20)}{"|":^3}{fmt(hyp, 20)}')

        dist, length = char_distance(ref, hyp)
        total_dist += dist
        total_length += length

    return total_dist, total_length, transcripts


@torch.no_grad()
def evaluate(model, data_loader, criterion, device, save_output=False):
    total_loss = 0.
    total_num = 0
    total_dist = 0
    total_length = 0
    total_sent_num = 0
    transcripts_list = []

    model.eval()
    for i, (data) in tqdm(enumerate(data_loader), total=len(data_loader)):
        feats, scripts, feat_lengths, script_lengths = data

        feats = feats.to(device)
        scripts = scripts.to(device)
        feat_lengths = feat_lengths.to(device)

        src_len = scripts.size(1)
        target = scripts[:, 1:]

        logit = model(feats, feat_lengths, None, teacher_forcing_ratio=0.0)
        logit = torch.stack(logit, dim=1).to(device)
        y_hat = logit.max(-1)[1]

        logit = logit[:, :target.size(1), :]  # cut over length to calculate loss
        loss = criterion(logit.contiguous().view(-1, logit.size(-1)), target.contiguous().view(-1))
        total_loss += loss.item()
        total_num += sum(feat_lengths).item()

        _, _, transcripts = get_distance(target, y_hat)
        # cer = float(dist / length) * 100

        # total_dist += dist
        # total_length += length
        if save_output == True:
            transcripts_list += transcripts
        total_sent_num += target.size(0)

    aver_loss = total_loss / total_num
    # aver_cer = float(total_dist / total_length) * 100
    return aver_loss, _, transcripts_list


def main():
    global char2index
    global index2char
    global SOS_token
    global EOS_token
    global PAD_token

    parser = argparse.ArgumentParser(description='LAS')
    parser.add_argument('--model-name', type=str, default='LAS')
    # Dataset
    parser.add_argument('--test-file-list', nargs='*',
                        help='data list about test dataset', default=['data/Youtube/clean'])
    parser.add_argument('--labels-path', default='data/kor_syllable.json',
                        help='Contains large characters over korean')
    parser.add_argument('--dataset-path', default='data/Youtube/clean', help='Target dataset path')

    # Hyperparameters
    parser.add_argument('--rnn-type', default='lstm', help='Type of the RNN. rnn|gru|lstm are supported')
    parser.add_argument('--encoder_layers', type=int, default=3, help='number of layers of model (default: 3)')
    parser.add_argument('--encoder_size', type=int, default=512, help='hidden size of model (default: 512)')
    parser.add_argument('--decoder_layers', type=int, default=2, help='number of pyramidal layers (default: 2)')
    parser.add_argument('--decoder_size', type=int, default=512, help='hidden size of model (default: 512)')
    parser.add_argument('--no-bidirectional', dest='bidirectional', action='store_false', default=True,
                        help='Turn off bi-directional RNNs, introduces lookahead convolution')
    parser.add_argument('--num_workers', type=int, default=4, help='Number of workers in dataset loader (default: 4)')
    parser.add_argument('--num_gpu', type=int, default=1, help='Number of gpus (default: 1)')
    parser.add_argument('--learning-anneal', default=1.1, type=float, help='Annealing learning rate every epoch')
    parser.add_argument('--max_len', type=int, default=80, help='Maximum characters of sentence (default: 80)')
    parser.add_argument('--max-norm', default=400, type=int, help='Norm cutoff to prevent explosion of gradients')

    # Audio Config
    parser.add_argument('--sample-rate', default=16000, type=int, help='Sampling Rate')
    parser.add_argument('--window-size', default=.02, type=float, help='Window size for spectrogram')
    parser.add_argument('--window-stride', default=.01, type=float, help='Window stride for spectrogram')

    # System
    parser.add_argument('--model-path', default='models/final.pth', help='Location to save best validation model')
    parser.add_argument('--seed', type=int, default=123456, help='random seed (default: 123456)')
    args = parser.parse_args()

    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    np.random.seed(args.seed)
    random.seed(args.seed)

    char2index, index2char = label_loader.load_label_json(args.labels_path)
    SOS_token = char2index['<s>']
    EOS_token = char2index['</s>']
    PAD_token = char2index['_']

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    audio_conf = dict(sample_rate=args.sample_rate,
                      window_size=args.window_size,
                      window_stride=args.window_stride)

    print(">> Test dataset : ", args.dataset_path)

    testData_list = []

    for wav_name in sorted(glob(f'{args.dataset_path}/*'), key=lambda i: int(os.path.basename(i)[:-4])):
        wav_dict = {}
        wav_dict['wav'] = os.path.basename(wav_name)
        wav_dict['text'] = os.path.basename(wav_name)
        wav_dict['speaker_id'] = '0'
        testData_list.append(wav_dict)

    test_dataset = SpectrogramDataset(audio_conf=audio_conf,
                                      dataset_path=args.dataset_path,
                                      data_list=testData_list,
                                      char2index=char2index, sos_id=SOS_token, eos_id=EOS_token,
                                      normalize=True)
    test_loader = AudioDataLoader(test_dataset, batch_size=1, num_workers=args.num_workers)

    input_size = int(math.floor((args.sample_rate * args.window_size) / 2) + 1)
    enc = EncoderRNN(input_size, args.encoder_size, n_layers=args.encoder_layers, bidirectional=args.bidirectional,
                     rnn_cell=args.rnn_type, variable_lengths=False)

    dec = DecoderRNN(len(char2index), args.max_len, args.decoder_size, args.encoder_size,
                     SOS_token, EOS_token,
                     n_layers=args.decoder_layers, rnn_cell=args.rnn_type, bidirectional_encoder=args.bidirectional)

    model = Seq2Seq(enc, dec)

    print("Loading checkpoint model %s" % args.model_path)
    state = torch.load(args.model_path)
    model.load_state_dict(state['model'])

    model = model.to(device)
    criterion = nn.CrossEntropyLoss(reduction='mean').to(device)

    print("Number of parameters: %d" % Seq2Seq.get_param_size(model))

    test_loss, test_cer, transcripts_list = evaluate(model, test_loader, criterion, device, save_output=True)

    print(f"{'true':^20} | {'pred':^20}")
    for line in transcripts_list:
        print(line)

    print("Test {} CER : {}".format("test", test_cer))


if __name__ == "__main__":
    main()
