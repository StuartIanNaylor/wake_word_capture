import glob
import argparse
import soundfile as sf
import numpy as np
import tensorflow as tf
import uuid
from scipy.io import wavfile

parser = argparse.ArgumentParser()
parser.add_argument('--libri_dir', default='./LibriSpeech/train-clean-100', help='source dir location default=./LibriSpeech/train-clean-100')
parser.add_argument('--target_length', type=float, default=1.0, help='Minimum trimmed length default=1.0s')
parser.add_argument('--window_stride', type=float, default=0.020, help='window_stride default=0.020')
parser.add_argument('--sample_rate', type=int, default=16000, help='Sample rate default=16000')
parser.add_argument('--kw_index', type=int, default=0, help='kw label index default=0')
parser.add_argument('--kw_sensitivity', type=float, default=0.40, help='kw_sensitivity default=0.50')
parser.add_argument('--model_path', default='../stream_state_external.tflite', help='tflite model path default=../stream_state_external.tflite')
args = parser.parse_args()

reset_count = 0
blocksize = int((args.sample_rate * args.target_length) * args.window_stride)
kw_length = int(args.sample_rate * args.target_length)
strides = int(kw_length / blocksize)
audio_buffer = np.zeros((1, kw_length * 2), dtype=np.float32)
kw_averages = np.zeros((1, strides), dtype=np.float32)
kw_sensitivity = args.kw_sensitivity
kw_max_avg = 0

interpreter = tf.lite.Interpreter(model_path=args.model_path)
#interpreter = tflite.Interpreter(model_path=args.model_path)
interpreter.allocate_tensors()
# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
inputs = []
for s in range(len(input_details)):
  inputs.append(np.zeros(input_details[s]['shape'], dtype=np.float32))
  
libri_files = glob.glob(args.libri_dir + '/**/*.flac', recursive=True)
#libri_files = glob.glob('/media/stuart/Linux-data/bcresnet/data/kw/*.wav')
if not libri_files:
  print("No Libri files found", args.libri_dir)
else:
  #print(libri_files)
  pass

for file_name in libri_files:
  flac_file, sample_rate = sf.read(file_name,dtype='float32')
  pos = 0
  while True:
    if pos + blocksize > len(flac_file):
      break
    rec = flac_file[pos:pos + blocksize]
    #print(rec)
    pos += blocksize
      
    if reset_count > 0:
      reset_count -= 1
      rec = np.zeros((1, blocksize), dtype=np.float32)
    else:
      rec = np.reshape(rec, (1, blocksize))
      audio_buffer = np.roll(audio_buffer, -blocksize)
      #print(audio_buffer.shape, rec.shape, kw_length, blocksize, audio_buffer.shape)
      audio_buffer[0,(kw_length * 2) - blocksize:kw_length * 2] = rec[0,:]

    # Make prediction from model
    interpreter.set_tensor(input_details[0]['index'], rec)
    # set input states (index 1...)
    for s in range(1, len(input_details)):
      interpreter.set_tensor(input_details[s]['index'], inputs[s])
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    # get output states and set it back to input states
    # which will be fed in the next inference cycle
    for s in range(1, len(input_details)):
      # The function `get_tensor()` returns a copy of the tensor data.
      # Use `tensor()` in order to get a pointer to the tensor.
      inputs[s] = interpreter.get_tensor(output_details[s]['index'])


    kw_averages = np.roll(kw_averages, -1)
    kw_averages[0, strides - 1] = output_data[0][0]
    kw_avg = np.ma.average(kw_averages, axis=1)[0]
    
    if kw_avg > kw_sensitivity:
      if kw_avg > kw_max_avg:
        kw_max_avg = kw_avg
      else:
        reset_count = int(strides / 2) + 1
        print(kw_max_avg, file_name)
        kw_max_avg = 0
        kw_averages = np.zeros((1, strides), dtype=np.float32)
        for s in range(len(input_details)):
          inputs.append(np.zeros(input_details[s]['shape'], dtype=np.float32))
        wavfile.write(str(uuid.uuid4()) + ".wav", sample_rate, audio_buffer[0][:])
      
    
