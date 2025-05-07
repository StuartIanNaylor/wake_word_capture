#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from scipy.io import wavfile
import sounddevice as sd
import numpy as np
import threading
import argparse
import uuid

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--list_devices', help='list input devices', action="store_true")
parser.add_argument('-i', '--device', type=int, help='Record device index --list_devices to list indexes')
parser.add_argument('--model_path', default='non_stream.tflite', help='tflite model path default=non_stream.tflite')
parser.add_argument('--kw_length', type=float, default=1.5, help='kw_length default=1.5')
parser.add_argument('--sample_rate', type=int, default=16000, help='Sample rate default=16000')
parser.add_argument('--windows', type=int, default=40, help='Sample rate default=10')
parser.add_argument('--kw_index', type=int, default=0, help='kw label index default=0')
parser.add_argument('--noise_index', type=int, default=4, help='noise label index default=1')
parser.add_argument('--kw_sensitivity', type=float, default=0.10, help='kw_sensitivity default=0.50')
parser.add_argument('--noise_sensitivity', type=float, default=0.99, help='noise_sensitivity default=0.90')
parser.add_argument('--debug', help='debug effect settings to cli', action="store_true")
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

num_channels = 1
kw_sensitivity = args.kw_sensitivity
kw_index = args.kw_index
noise_sensitivity = args.noise_sensitivity
noise_index = args.noise_index
blocksize = int(args.sample_rate * args.kw_length)
window_size = int(blocksize / args.windows)
windows = args.windows

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
rolling_window = np.zeros((1, blocksize), dtype=np.float32)
averages = np.zeros((1, windows), dtype=np.float32)
audio_buffer = np.zeros((1, blocksize * 2), dtype=np.float32)
max_avg = 0

def sd_callback(rec, frames, ftime, status):

  global reset_state, reset_count, blocksize, window_size, rolling_window, windows
  global kw_sensitivity, noise_sensitivity, input_details, output_details, inputs
  global averages, max_avg, audio_buffer, sample_rate

  rec = np.reshape(rec, (1, window_size))
  audio_buffer = np.roll(audio_buffer, -window_size)
  audio_buffer[0,(blocksize * 2) - window_size:blocksize * 2] = rec[0,:]
  # Notify if errors
  if status:
    print('Error:', status)
    
  if reset_count > 0:
    reset_count -= 1
  else:
    rolling_window = np.roll(rolling_window, -window_size)
    rolling_window[0,blocksize - window_size:blocksize] = rec[0,:]
           
    # set input audio data (by default input data at index 0)
    interpreter.set_tensor(input_details[0]['index'], rolling_window)

    # run inference
    interpreter.invoke()

    # get output: classification
    out_tflite = interpreter.get_tensor(output_details[0]['index'])
    out_tflite_argmax = np.argmax(out_tflite[0])
    averages = np.roll(averages, -1)
    averages[0, windows - 1] = out_tflite[0][0]
        
    avg = np.ma.average(averages, axis=1)[0]   
    #0 kw, 1 falsekw, 2 notkw, 3 phonekw, 4 noise check labels.txt

    if avg > kw_sensitivity:
      if avg > max_avg:
        max_avg = avg
      else:
        reset_count = int(windows / 2) + 1
        print(max_avg)
        max_avg = 0
        rolling_window = np.zeros((1, blocksize), dtype=np.float32)
        averages = np.zeros((1, windows), dtype=np.float32)
        wavfile.write(str(uuid.uuid4()), sample_rate, audio_buffer[0][:])
     #if out_tflite_argmax == 4 and out_tflite[0][4] > noise_sensitivity:
       #print(4, out_tflite[0][4])
    

          

print("Loaded")

# Start streaming from microphone
with sd.InputStream(channels=num_channels,
                    samplerate=args.sample_rate,
                    blocksize=window_size,
                    callback=sd_callback):

  threading.Event().wait()    

