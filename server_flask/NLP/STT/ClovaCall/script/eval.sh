#!/bin/bash

MAIN_DIR=${0%/*}
cd $MAIN_DIR/..

TARGET_CODE=las.pytorch/eval.py
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

DATA=$1

if [ -n {$2} ]; then
  TEST_FILE=data/${DATA}/test_${DATA}.json
else
  TEST_FILE=data/${DATA}/test_${DATA}_few.json
fi

LABEL_FILE=data/kor_syllable.json
if [ ${DATA} = "AIhub" ]; then
  DATASET_PATH=data/${DATA}/KsponSpeech
else
  DATASET_PATH=data/${DATA}/clean
fi

CUDA_DEVICE_ID=1

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
  --test-file-list $TEST_FILE \
  --labels-path $LABEL_FILE \
  --dataset-path $DATASET_PATH \
  --model-path models/final.pth
