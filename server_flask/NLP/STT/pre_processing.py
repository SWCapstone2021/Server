import librosa
import numpy as np
import torch
import torchaudio
from torch import Tensor


def get_duration(audio, sr):
    return librosa.core.get_duration(audio, sr=sr)


def get_silence(sec, sr):
    return np.zeros(sr * sec)


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
        duration = get_duration(segment, sr)

        if duration <= min_segment_length:
            continue

        padded_segment = np.concatenate([
            get_silence(1, sr),
            segment,
            get_silence(1, sr),
        ])

        signals.append(padded_segment)
        time_stamps.append(int(start / sr))

    return signals, time_stamps


def parse_audio(audio_path: str):
    signals, time_stamps = split_on_silence_with_librosa(audio_path)
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
