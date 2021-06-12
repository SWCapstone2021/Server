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
from basefunction.FindUMethod import MakeFile

warnings.filterwarnings('ignore')

os.environ["CUDA_VISIBLE_DEVICES"] = "2"

sr = 16000
device = 'cuda' if torch.cuda.is_available else 'cpu'
model_name = 'ds2'
print(f"{model_name} model loading...")
model, vocab = load_model(model_path=f'STT/models/{model_name}.pt')
print("Done")


def save_audio(signals, sr):
    for i, signal in enumerate(signals):
        soundfile.write(f'data/audio/{i}.wav', signal, sr, format='WAV', endian='LITTLE', subtype='PCM_16')


def make_scripts(ids):
    for id in ids:
        if not os.path.exists(f'data/origin_audio/{id}.wav') or not os.path.exists(f'data/scripts/{id}.ko.vtt'):
            print(f"Make scripts about {id}")
            MakeFile(f'https://www.youtube.com/watch?v={id}')


def get_duration(audio):
    return librosa.core.get_duration(audio, sr=sr)


def get_silence(sec):
    return np.zeros(sr * sec)


def load_audio(path, pre_silence_length=0, post_silence_length=0):
    audio = librosa.core.load(path, sr=sr)[0]
    if pre_silence_length > 0 or post_silence_length > 0:
        audio = np.concatenate([
            get_silence(pre_silence_length),
            audio,
            get_silence(post_silence_length),
        ])
    return audio


def abs_mean(x):
    return abs(x).mean()


def remove_breath(audio):
    edges = librosa.effects.split(
        audio, top_db=40, frame_length=128, hop_length=32)

    for idx in range(len(edges)):
        start_idx, end_idx = edges[idx][0], edges[idx][1]
        if start_idx < len(audio):
            if abs_mean(audio[start_idx:end_idx]) < abs_mean(audio) - 0.05:
                audio[start_idx:end_idx] = 0

    return audio


def split_on_silence_with_librosa(
        audio_path, top_db=40, frame_length=1024, hop_length=256,
        skip_idx=0, min_segment_length=0.5):
    audio, sr = librosa.load(audio_path, sr=16000)

    edges = librosa.effects.split(audio,
                                  top_db=top_db, frame_length=frame_length, hop_length=hop_length)

    new_audio = np.zeros_like(audio)
    for idx, (start, end) in enumerate(edges[skip_idx:]):
        new_audio[start:end] = remove_breath(audio[start:end])

    audio = new_audio
    edges = librosa.effects.split(audio,
                                  top_db=top_db, frame_length=frame_length, hop_length=hop_length)

    signals = list()
    time_stamps = list()
    for idx, (start, end) in enumerate(edges[skip_idx:]):
        segment = audio[start:end]
        duration = get_duration(segment)

        if duration <= min_segment_length:
            continue

        padded_segment = np.concatenate([
            get_silence(1),
            segment,
            get_silence(1),
        ])

        signals.append(padded_segment)
        time_stamps.append(int(start / sr))

    return signals, time_stamps


def list_stt(ids):
    true_label = list()
    youtube_label = list()
    our_label = list()

    for id in ids:
        print(id)
        audio_path = f'data/origin_audio/clean/{id}.wav'
        true_script = open(f'data/true/{id}.txt').read().splitlines()
        script = open(f'data/script/{id}.ko.vtt').read().splitlines()[4:]

        subscribe = list()
        for idx in range(0, len(script), 3):
            subscribe.append(script[idx + 1])

        features, input_lengths, time_stamps = parse_audio(audio_path)

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


def parse_audio(audio_path):
    signals, time_stamps = split_on_silence_with_librosa(audio_path)
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
    ids = [os.path.basename(x)[:-4] for x in glob('data/true_one/*')]

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
