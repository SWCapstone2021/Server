# -*- coding: utf-8 -*-
from pytube import YouTube
import youtube_dl
import os
import glob
from os.path import basename
from konlpy.tag import Mecab
from math import log

#YOUTUBE_REPO_PATH = '/home/heesu/mount/NLP/script'


# def MakeVttFile(URL, auto_sub=False):
#     DownOption = {
#         'skip_download': True,
#         'writesubtitles': True,
#         'writeautomaticsub': auto_sub,
#         'subtitleslangs': ['ko'],
#         'subtitlesformat': 'vtt',
#         'nooverwrites': True,
#         'outtmpl': 'script/%(id)s'
#     }
#     with youtube_dl.YoutubeDL(DownOption) as ydl:
#         ydl.download([URL])
#         ChkFile(URL)


# def ChkFile(URL):
#     if not os.path.exists(f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.vtt'):
#         MakeVttFile(URL, auto_sub=True)
#         SubtitleFile = f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.vtt'
#         f = open(SubtitleFile, 'r')
#         lines = f.readlines()
#         f.close()
#         fw = open(SubtitleFile, 'w')
#         for line in lines[:4]:
#             fw.write(line)
#         for idx, line in enumerate(lines[6::8]):
#             skip = False
#             time_stamp = True
#             clean = ''
#             time = ''
#             for c in line:
#                 if c == '>':
#                     skip = False
#                     time_stamp = False
#                     continue

#                 if c == '<' or skip:
#                     if time_stamp and skip:
#                         time += c
#                     skip = True
#                     continue

#                 clean += c
#             if time_stamp:
#                 try:
#                     time = lines[(idx+1)*8].split(' ')[0]
#                 except:
#                     pass
#             fw.write(f'{time}\n{clean}\n')
#         fw.close()


# def MakeTXTFile(URL):
#     SubtitleFile = f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.vtt'
#     f = open(SubtitleFile, 'r')
#     lines = f.readlines()
#     entire_text = ''
#     for line in lines[5::3]:
#         entire_text += line
#     f.close()
#     fw = open('%s.txt' % (SubtitleFile[:-4]), 'w')
#     fw.write(entire_text)
#     fw.close()


# def ChkID(URL):
#     id = URL.rsplit('/', 1)[-1]
#     return id


def Ctrl_F(keyword, video_data):
    TimeStamp = []
    StartPoint = 0

    for per_data in video_data:
        script = per_data['text'].replace('\n', '')
        if keyword in script:
            TimeStamp.append(
                {
                    "script": script,
                    "start": per_data['start']})
    return TimeStamp


# def ChkTxtFile(URL):
#     if not os.path.exists(f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.txt'):
#         MakeTXTFile(URL)


# def Noun(URL):
#     ChkTxtFile(URL)
#     with open(f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.txt', 'r', encoding='utf-8') as f:
#         script = f.read()
#     mecab = Mecab()
#     NounResult = mecab.nouns(script)
#     return NounResult


def Frequency(keyword, script):
    TF = 0
    for word in script:
        word = word['text']
        if keyword in word:
            TF += 1
    ILF = 0
    for line in script:
        line = line['text']
        if keyword in line:
            ILF += 1

    if ILF == 0:
        TF_IDF = 0
    else:
        TF_IDF = TF * log(len(script) / ILF)

    return round(TF_IDF, 2)
    # TF-IDF = TF * (log(N/df)) TF:단어 빈도수, N: 문장개수, IDF: 단어가 포함된 문장개수
