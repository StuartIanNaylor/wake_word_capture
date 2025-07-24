#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#import tflite_runtime.interpreter as tflite
import tensorflow as tf
import numpy as np
import soundfile as sf
import os
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--model_path', default='non_stream.tflite', help='tflite model path default=non_stream.tflite')
parser.add_argument('--source_path', default='./out', help='kw sample files path default=./out')                
parser.add_argument('--label_index', type=int, default=0, help='kw label index of hit test default=0')
parser.add_argument('--kw_length', type=float, default=1.0, help='length of kw (secs) default=1.0')
parser.add_argument('--sample_rate', type=int, default=16000, help='Sample rate default=16000')
parser.add_argument('--prob_file', default='./prob.txt', help='Sample file prob results default=./prob.txt')
args = parser.parse_args()

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
sample_length = int(args.kw_length * args.sample_rate)

interpreter = tf.lite.Interpreter(model_path=args.model_path)
#interpreter = tflite.Interpreter(model_path=args.model_path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
inputs = []
for s in range(len(input_details)):
  inputs.append(np.zeros(input_details[s]['shape'], dtype=np.float32))

prob = open(args.prob_file,"w")  
count = 0    
source = glob.glob(os.path.join(args.source_path, '*.wav'))
print("Testing " + str(len(source)), args.source_path)
for filename in source:
  wav, samplerate = sf.read(filename,dtype='float32')
  if len(wav) > sample_length:
    offset = len(wav) - sample_length
    rnd_start = random.randrange(0, offset)
    wav = wav[rnd_start:rnd_start+sample_length]
  wav = np.reshape(wav, (1, sample_length))
  # set input audio data (by default input data at index 0)
  interpreter.set_tensor(input_details[0]['index'], wav.astype(np.float32))
  # run inference
  interpreter.invoke()
  # get output: classification
  out_tflite = interpreter.get_tensor(output_details[0]['index'])
  #0 kw, 1 falsekw, 2 notkw, 3 noise check labels.txt
  hit = out_tflite[0][args.label_index]

  prob.write(filename + "," + str(hit) + "\n")
  count += 1
print("total found " + str(count), len(source), args.source_path)
prob.close()

