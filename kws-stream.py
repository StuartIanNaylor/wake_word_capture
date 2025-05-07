#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
import sounddevice as sd
from scipy.io import wavfile
import numpy as np
import threading
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--device', type=int, help='Record device index --list_devices to list indexes')
parser.add_argument('--model_path', default='stream_state_external_quant.tflite', help='tflite model path default=stream_state_external_quant.tflite')
parser.add_argument('--window_stride', type=float, default=0.020, help='window_stride default=0.020')
parser.add_argument('--sample_rate', type=int, default=16000, help='Sample rate default=16000')
parser.add_argument('--kw_length', type=float, default=1.5, help='kw_length default=1.5')
parser.add_argument('--kw_index', type=int, default=0, help='kw label index default=0')
parser.add_argument('--noise_index', type=int, default=1, help='noise label index default=1')
parser.add_argument('--kw_sensitivity', type=float, default=0.90, help='kw_sensitivity default=0.70')
parser.add_argument('--list_devices', help='list input devices', action="store_true")
parser.add_argument('--noise_sensitivity', type=float, default=0.90, help='noise_sensitivity default=0.90')
args = parser.parse_args()
 
if args.list_devices:
 print(sd.query_devices())
 exit()
 
num_channels = 1
sample_rate = args.sample_rate

if args.device:
  print(sd.query_devices(device=args.device, kind='input'))
  sd.default.device = args.device
  sd.default.samplerate = sample_rate
  sd.default.channels = num_channels, None
  
#from ai_edge_litert.interpreter import Interpreter
#import tflite_runtime.interpreter as tflite
import tensorflow as tf

blocksize = int(sample_rate * args.kw_length)
stride = args.window_stride
stride_length = int(sample_rate * stride)
strides = int(blocksize * stride) 
kw_index = args.kw_index
noise_index = args.noise_index
kw_sensitivity = args.kw_sensitivity
# Load the TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path=args.model_path)
#interpreter = tflite.Interpreter(model_path=args.model_path)
interpreter.allocate_tensors()
# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
inputs = []
for s in range(len(input_details)):
  inputs.append(np.zeros(input_details[s]['shape'], dtype=np.float32))
  
reset_count = 0
audio_buffer = np.zeros((1, blocksize * 2), dtype=np.float32)
  
def sd_callback(rec, frames, ftime, status):
     
    global kw_index,noise_index, stride_length, strides, kw_sensitivity
    global interpreter, input_details, output_details, inputs, reset_count, audio_buffer
    # Notify if errors
    if status:
        print('Error:', status)
    rec = np.reshape(rec, (1, stride_length))
    audio_buffer[0,(blocksize * 2) - stride_length:blocksize * 2] = rec[0,:]
    audio_buffer = np.roll(audio_buffer, -stride_length)
    

    if reset_count > 0:
      reset_count -= 1
      for s in range(len(input_details)):
        inputs.append(np.zeros(input_details[s]['shape'], dtype=np.float32))
      rec = np.zeros((1, stride_length), dtype=np.float32)

    # Make prediction from model
    interpreter.set_tensor(input_details[0]['index'], rec)
    # set input states (index 1...)
    for s in range(1, len(input_details)):
      interpreter.set_tensor(input_details[s]['index'], inputs[s])
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    # get output states and set it back to input states
    # which will be fed in the next inference cycle
    if output_data[0][0] > kw_sensitivity and reset_count < 1:
      print(0, output_data[0][0])
      reset_count = int(strides / 2) + 1
      for s in range(len(input_details)):
        inputs.append(np.zeros(input_details[s]['shape'], dtype=np.float32))
      wavfile.write(str(uuid.uuid4()) + ".wav", sample_rate, audio_buffer[0][:])
    else:
      for s in range(1, len(input_details)):
        # The function `get_tensor()` returns a copy of the tensor data.
        # Use `tensor()` in order to get a pointer to the tensor.
        inputs[s] = interpreter.get_tensor(output_details[s]['index'])
    sd.wait()
               
print("Loaded")
    
# Start streaming from microphone
with sd.InputStream(channels=num_channels,
                    samplerate=sample_rate,
                    blocksize=stride_length,
                    callback=sd_callback):
  threading.Event().wait()                        
