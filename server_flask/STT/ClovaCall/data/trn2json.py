import json
import os
import re
from collections import OrderedDict
from glob import glob

from tqdm import tqdm

kspon_1 = (0, 124000)
kspon_2 = (124001, 248000)
kspon_3 = (248001, 372000)
kspon_4 = (372001, 496000)
kspon_5 = (496001, 622545)
kspon_list = [kspon_1, kspon_2, kspon_3, kspon_4, kspon_5]


def where_is_wav(num_file):
    num_file = int(num_file)
    for idx, kspon in enumerate(kspon_list):
        if num_file <= kspon[1] and num_file >= kspon[0]:
            return f'KsponSpeech_0{idx+1}'
    return 'NO'

def remove_bracket(text):
    _q_list = []
    cnt = 0
    for i, w in enumerate(text):
        cnt += 1
        if w == '(':
            _q_list.append(i)
        if w == ')':
            _q_list.append(i)

    if len(_q_list) == 0:
        return text

    q_list = []
    for x in range(len(_q_list)):
        if x % 2 == 0:
            q_list.append((_q_list[x], _q_list[x + 1]))

    reform_text = ''
    for i, q in enumerate(q_list):
        if i % 2 == 0:
            if i == 0:
                reform_text += text[:q[0]] + text[q[0] + 1:q[1]]
            else:
                reform_text += text[q[0] + 1:q[1]]
        else:
            if i + 1 == len(q_list):
                continue
            reform_text += text[q[1] + 1:q_list[i + 1][0]]

    return reform_text


for file_name in tqdm(glob('AIhub/*.trn')):

    json_list = []
    with open(file_name, 'r', encoding='utf-8') as f:
        for x in f.read().splitlines():
            wav, text = x.split('/', 2)[-1].split(" :: ")
            wav = wav.replace('pcm', 'wav')
            text = re.sub("b/|l/|o/|n/|/|\+", "", text)

            try:
                num_file = wav.split('_')[1].split('.')[0]

                base_dir = where_is_wav(num_file)
                if base_dir == 'NO':
                    continue

            except:
                num_file = wav.split('E')[1].split('.')[0]
                base_dir = 'KsponSpeech_Eval'

            text = text.strip()
            text_length = len(text)
            if text_length < 3 or text_length > 128:
                continue

            text = remove_bracket(text)

            json_data = OrderedDict()
            json_data["wav"] = f'{base_dir}/{wav}'
            json_data["text"] = text
            json_data["speaker_id"] = "0"
            json_list.append(json_data)

    with open(file_name.replace('trn', 'json'), 'w', encoding='utf-8') as make_file:
        json.dump(json_list, make_file, ensure_ascii=False, indent='\t')

    # os.remove(file_name)
