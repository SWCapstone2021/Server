#!/bin/bash

MAIN_DIR=${0%/*}
cd $MAIN_DIR/..

LABEL_FILE=data/kor_syllable.json
TARGET_CODE=las.pytorch/folder_eval.py
MODEL_PATH=models

if [ ! -f $TARGET_CODE ]; then
  echo "[ERROR] TARGET_CODE($TARGET_CODE) not found."
  exit
fi

if [ ! -d $MODEL_PATH ]; then
  mkdir $MODEL_PATH
fi

if [ ! -d $LOG_PARENT_PATH ]; then
  mkdir $LOG_PARENT_PATH
fi

################################################################
##	Careful while modifying lines above.
################################################################
CUDA_DEVICE_ID=4

# Default
RNN_TYPE=LSTM

# LAS
ENCODER_LAYERS=3
ENCODER_SIZE=512
DECODER_LAYERS=2
DECODER_SIZE=512

GPU_SIZE=1
CPU_SIZE=4

################################################################
##	Careful while modifying lines below.
################################################################

CUDA_VISIBLE_DEVICES=$CUDA_DEVICE_ID \
  python -u $TARGET_CODE \
  --num_workers $CPU_SIZE \
  --num_gpu $GPU_SIZE \
  --rnn-type $RNN_TYPE \
  --encoder_layers $ENCODER_LAYERS --encoder_size $ENCODER_SIZE \
  --decoder_layers $DECODER_LAYERS --decoder_size $DECODER_SIZE \
  --labels-path $LABEL_FILE \
  --model-path models/final.pth
