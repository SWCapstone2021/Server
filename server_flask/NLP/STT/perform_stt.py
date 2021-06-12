import os
import warnings
from glob import glob

import Levenshtein as Lev
import librosa
import numpy as np
import soundfile
import torch
import torchaudio
from torch import Tensor

from STT import load_model
from STT.hanspell import spell_checker
from STT.kospeech.models import (
    DeepSpeech2,
    ListenAttendSpell,
)

warnings.filterwarnings('ignore')

os.environ["CUDA_VISIBLE_DEVICES"] = "2"

device = 'cuda' if torch.cuda.is_available else 'cpu'
model_name = 'ds2'
print(f"{model_name} model loading...")
model, vocab = load_model(model_path=f'models/{model_name}.pt')
print("Done")


def save_audio(signals, sr):
    for i, signal in enumerate(signals):
        soundfile.write(f'data/audio/{i}.wav', signal, sr, format='WAV', endian='LITTLE', subtype='PCM_16')


def __split_with_value(y, sr, intervals):
    len_interval = len(intervals)
    signals = list()
    time_stamps = list()

    i = 0
    while i < len_interval - 1:
        start = intervals[i] - 9000
        end = intervals[i + 1] - 9000
        if start < 0:
            start = 0
        wav = y[int(start):int(end)]
        signals.append(wav)
        time_stamps.append(int(start) / sr)
        i += 1

    wav = y[int(intervals[i]):]
    signals.append(wav)
    time_stamps.append(int(intervals[i]) / sr)

    return signals, time_stamps


def list_stt(ids):
    true_label = list()
    youtube_label = list()
    our_label = list()

    for id in ids:
        print(id)
        audio_path = f'data/origin_audio/{id}.wav'
        true_script = open(f'data/true/{id}.txt').read().splitlines()
        script = open(f'data/script/{id}.ko.vtt').read().splitlines()[4:]

        times = list()
        subscribe = list()
        for idx in range(0, len(script), 3):
            times.append(string_to_ms(script[idx]))
            subscribe.append(script[idx + 1])

        features, input_lengths, time_stamps = parse_audio(audio_path, times)

        sentences = list()

        if isinstance(model, ListenAttendSpell):
            model.encoder.device = device
            model.decoder.device = device

        elif isinstance(model, DeepSpeech2):
            model.device = device

        for feature, input_length, time_stamp in zip(features, input_lengths, time_stamps):
            y_hats = model.recognize(feature.unsqueeze(0).to(device), input_length)
            sentence = vocab.label_to_string(y_hats.cpu().detach().numpy())
            sentences.append(spell_checker.check(sentence[0]).checked)

        our_label.append(sentences)
        true_label.append(true_script)
        youtube_label.append(subscribe)

    return true_label, youtube_label, our_label


def parse_audio(audio_path, times):
    signal, sr = librosa.load(audio_path, sr=16000)
    signals, time_stamps = __split_with_value(signal, sr, times)
    features = list()
    input_lengths = list()

    save_audio(signals, sr)

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


def string_to_ms(string: str):
    times = string.split(':')
    hour, minute, second = int(times[0]), int(times[1]), float(times[2])

    return hour * 60 * 60 * 16000 + minute * 60 * 16000 + second * 16000


def char_distance(ref, hyp):
    ref = ref.replace(' ', '')
    hyp = hyp.replace(' ', '')

    dist = Lev.distance(hyp, ref)
    length = len(ref.replace(' ', ''))

    return dist, length


def calculate_CER(y, y_hat):
    total_dist = 0
    total_length = 0
    for ref, hyp in zip(y, y_hat):
        dist, length = char_distance(ref, hyp)
        total_dist += dist
        total_length += length

    cer = float(total_dist / total_length) * 100
    return cer


if __name__ == "__main__":
    ids = [os.path.basename(x)[:-4] for x in glob('data/true/*')]

    # make_scripts(ids)
    true_label, youtube_label, our_label = list_stt(ids)

    print("id | youtube cer | out cer | result")

    for tl, yl, ol, id in zip(true_label, youtube_label, our_label, ids):
        youtube_cer = calculate_CER(tl, yl)
        our_cer = calculate_CER(tl, ol)
        print(f"{id} : {youtube_cer}% | {our_cer}% | {'WIN' if our_cer < youtube_cer else 'LOSE'}")

        f = open(f"data/result/{id}.txt", 'w')
        for y, o in zip(yl, ol):
            f.write(y + '\n')
            f.write(o + '\n')
            f.write('======\n')
        f.close()
