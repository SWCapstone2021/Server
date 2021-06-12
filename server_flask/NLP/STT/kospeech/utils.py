import logging
import platform

import librosa
import soundfile
import torch

logger = logging.getLogger(__name__)


def check_envirionment(use_cuda: bool) -> torch.device:
    """
    Check execution envirionment.
    OS, Processor, CUDA version, Pytorch version, ... etc.
    """
    cuda = use_cuda and torch.cuda.is_available()
    device = torch.device('cuda' if cuda else 'cpu')

    logger.info(f"Operating System : {platform.system()} {platform.release()}")
    logger.info(f"Processor : {platform.processor()}")

    if str(device) == 'cuda':
        for idx in range(torch.cuda.device_count()):
            logger.info(f"device : {torch.cuda.get_device_name(idx)}")
        logger.info(f"CUDA is available : {torch.cuda.is_available()}")
        logger.info(f"CUDA version : {torch.version.cuda}")
        logger.info(f"PyTorch version : {torch.__version__}")

    else:
        logger.info(f"CUDA is available : {torch.cuda.is_available()}")
        logger.info(f"PyTorch version : {torch.__version__}")

    return device


def split_sound_n_save(file_name='data/sound.wav', base_dir='temp'):
    y, sr = librosa.load(file_name, sr=16000)

    intervals = librosa.effects.split(y, 25)

    len_interval = len(intervals)
    signals = list()
    time_stamps = list()

    i = 0
    while i < len_interval - 1:

        next_i = i
        while intervals[next_i][1] - intervals[next_i][0] < sr * 3 and intervals[next_i][0] - intervals[i][
            0] < sr * 5:
            next_i += 2
            if next_i > len_interval - 1:
                next_i = len_interval - 1
                break

        if i == next_i:
            next_i += 1

        wav = y[intervals[i][0]:intervals[next_i][0]]
        signals.append(wav)
        time_stamps.append(intervals[i][0] / sr)

        i = next_i

    for i, (wav, time) in enumerate(zip(signals, time_stamps)):
        soundfile.write(f'{base_dir}/{time}.wav', wav, sr, format='WAV', endian='LITTLE',
                        subtype='PCM_16')
