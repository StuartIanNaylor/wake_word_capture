#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import argparse
import glob
import os, operator, sys
import random
import soundfile as sf
import uuid
import sox
import configparser as CP
import math
import shortuuid
import gpuRIR
from scipy.io import wavfile
from scipy.signal import fftconvolve
import numpy as np

def augment(dest_dir, target_qty, target_length, debug, noise_dir, noise_vol, silent_percent, silent_vol):

  if not os.path.exists(noise_dir):
    print("Source_dir = " + noise_dir + " does not exist!")
    exit()
  if debug == 0:  
    logging.getLogger('sox').setLevel(logging.ERROR)
  else:
    logging.getLogger('sox').setLevel(logging.DEBUG)
    
  sample_rate = 16000
  gpuRIR.activateMixedPrecision(False)
  gpuRIR.activateLUT(True)
  print(noise_dir)
  noise_samples = glob.glob(os.path.join(noise_dir, '*.wav'))
  noise_qty = len(noise_samples)  
  sample_qty = math.ceil(target_qty / noise_qty)
  print(sample_qty)
  #exit()
  if noise_qty < 1:
    print("No noise files found *.wav")
    exit()
  if not os.path.exists(dest_dir):
    print("dest dir is missing")
    exit()
  if not os.path.exists('effects.ini'):
    print("effects.ini is missing")
    exit()
  
  cfg = CP.ConfigParser()
  cfg.read('effects.ini')
  count = 0
  for noise_wav in noise_samples:
    qty = 0
    while qty < sample_qty:
      if os.path.splitext(noise_wav)[1] == ".wav":
        augment_wav(noise_wav, dest_dir, cfg, sample_rate, target_length, qty + 1, noise_wav, noise_vol, silent_percent, silent_vol)
        qty += 1
        count += 1
        if count == target_qty:
          quit()
      else:
        print(noise_wav + ' is not a .wav')

def augment_wav(wav, dest_dir, cfg, sample_rate, target_length, version, noise_wav, noise_vol, silent_percent, silent_vol):
    
    target_samples = int(sample_rate * target_length)
    noise_length = sox.file_info.duration(noise_wav)
    if noise_length > target_length + 0.2:
      offset = (noise_length - (target_length + 0.2)) * random.random()
    else:
      print("Noise file to short for target length")
    tfm2 = sox.Transformer()
    tfm2.clear_effects()
    tfm2.trim(offset, target_length + offset + 0.2)
    tfm2.norm(-2)
    rand_effect = random.random()
    #wav_length = sox.file_info.duration(wav)
    target_samples = int(sample_rate * target_length)

    str_effect = ""
    if rand_effect < 0.33:
      pitch = random.randrange(int(cfg['pitch']['n_semitones_min']), int(cfg['pitch']['n_semitones_max'])) / 1000
      tfm2.pitch(n_semitones=pitch)
      str_effect = str_effect + "-pit"

    elif rand_effect < 0.66:
      tempo = random.randrange(int(cfg['tempo']['factor_min']), int(cfg['tempo']['factor_max'])) / 1000
      tfm2.tempo(factor=tempo, audio_type='s')
      str_effect = str_effect + "-tem"

    elif rand_effect < 1:
      speed = random.randrange(int(cfg['speed']['factor_min']), int(cfg['speed']['factor_max'])) / 1000
      tfm2.speed(factor=speed)
      str_effect = str_effect + "-spd"


    rand_effect = random.random()
    if rand_effect < 0.5:
      gain = random.randrange(int(cfg['treble']['gain_min']), int(cfg['treble']['gain_max'])) / 1000
      freq = random.randrange(int(cfg['treble']['freq_min']), int(cfg['treble']['freq_max'])) / 10
      slope = random.randrange(int(cfg['treble']['slope_min']), int(cfg['treble']['slope_max'])) / 1000
      tfm2.treble(gain_db=gain, frequency=freq, slope=slope)
      str_effect = str_effect + "-t"

    rand_effect = random.random()
    if rand_effect < 0.5:
      gain = random.randrange(int(cfg['bass']['gain_min']), int(cfg['bass']['gain_max'])) / 1000
      freq = random.randrange(int(cfg['bass']['freq_min']), int(cfg['bass']['freq_max'])) / 100
      slope = random.randrange(int(cfg['bass']['slope_min']), int(cfg['bass']['slope_max'])) / 1000
      tfm2.bass(gain_db=gain, frequency=freq, slope=slope)
      str_effect = str_effect + "-b"
    tfm2.build_file(noise_wav, '/tmp/noise.wav')
    
    noise_length = sox.file_info.duration('/tmp/noise.wav')
    #print(noise_length)
    tfm2.clear_effects()
    if noise_length < target_length:
        os.rename('/tmp/noise.wav', '/tmp/short-noise.wav')
        tfm2.pad(0, (0.1 + target_length) - noise_length)
        tfm2.build_file('/tmp/short-noise.wav', '/tmp/noise.wav')


    rwidth = random.randint(250, 800) / 100
    rlength = random.randint(250, 800) / 100
    rheight = random.randint(210, 300) / 100
    room_sz = [rwidth,rlength,rheight] 
    nb_rcv = 1    

    reciever_type = random.random()
    if reciever_type < 0.15:
        #leftwall
        #print("leftwall")
        orV_rcv = np.array([[1,0,0]])
        mic_pattern = "omni"
        rec_width = rwidth - (rwidth * (random.randint(95, 99) / 100))
        rec_height = rheight - (rheight * (random.randint(40, 80) / 100))
        rec_length = rlength - (rlength * (random.randint(30, 70) / 100))
        pos_rcv = np.array([[rec_width, rec_length, rec_height]])
    elif reciever_type < 0.3:
        #rightwall
        #print("rightwall")
        orV_rcv = np.array([[-1,0,0]])
        mic_pattern = "omni"
        rec_width = rwidth - (rwidth * (random.randint(1, 5) / 100))
        rec_height = rheight - (rheight * (random.randint(40, 80) / 100))
        rec_length = rlength - (rlength * (random.randint(30, 70) / 100))
        pos_rcv = np.array([[rec_width, rec_length, rec_height]])     
    elif reciever_type < 0.45:
        #frontwall
        #print("frontwall")
        orV_rcv = np.array([[0,1,0]])
        mic_pattern = "omni"
        rec_width = rwidth - (rwidth * (random.randint(30, 70) / 100))
        rec_height = rheight - (rheight * (random.randint(30, 95) / 100))
        rec_length = rlength - (rlength * (random.randint(1, 5) / 100))
        pos_rcv = np.array([[rec_width, rec_length, rec_height]])
    elif reciever_type < 0.6:
        #ceilling
        #print("ceiling")
        orV_rcv = np.array([[0,0,-1]])
        mic_pattern = "omni"
        rec_width = rwidth - (rwidth * (random.randint(30, 70) / 100))
        rec_height = rheight - (rheight * (random.randint(1, 5) / 100))
        rec_length = rlength - (rlength * (random.randint(30, 70) / 100))
        pos_rcv = np.array([[rec_width, rec_length, rec_height]])      
    else:
        #table
        #print("table")
        orV_rcv = np.array([[0,-1,0]])
        mic_pattern = "omni"
        rec_width = rwidth - (rwidth * (random.randint(5, 95) / 100))
        rec_height = rheight - (rheight * (random.randint(30, 70) / 100))
        rec_length = rlength - (rlength * (random.randint(20, 80) / 100))
        pos_rcv = np.array([[rec_width, rec_length, rec_height]])
        
    #print(pos_rcv, room_sz)
    if (rwidth * rlength * rheight) > (6 * 6 * 2.6):
        #large
        T60 = random.randint(400, 600) / 1000
        str_effect = str_effect + "-lrg" + str(T60)
    else:
        #small
        T60 = random.randint(200, 400) / 1000
        str_effect = str_effect + "-sml" + str(T60)
        
    att_diff = 15.0	# Attenuation when start using the diffuse reverberation model [dB]
    att_max = 60.0 # Attenuation at the end of the simulation [dB]
    fs=16000.0 # Sampling frequency [Hz]
    abs_weights = [0.9]*5+[0.5] # Absortion coefficient ratios of the walls
          
    source_type = random.random()
    if source_type < 0.25:
        #stereo
        nb_src = 2
        sourceheight = rheight - rheight * (random.randint(300, 900) / 1000) 
        pos_src = np.array([[rwidth * 0.25,0.3,sourceheight],[rwidth * 0.75,0.3,sourceheight]])
        spkr_pattern = "card"
        orV_src = np.array([[0,1,0], [0,1,0]])
    elif source_type < 0.5:
        #tv
        nb_src = 2
        sourceheight = rheight * 0.5
        pos_src = np.array([[rwidth * 0.33,0.05,sourceheight],[rwidth * 0.66,0.05,sourceheight]])
        spkr_pattern = "card"
        orV_src = np.array([[0,1,0], [0,1,0]])
    elif source_type < 0.75:
        #radio
        nb_src = 1
        sourceheight = rheight - rheight * (random.randint(30, 90) / 100)    
        pos_src = np.array([[rwidth * random.random(),rlength * random.random(),sourceheight]])
        spkr_pattern = "omni"
        orV_src = None
    else:
        #appliance
        nb_src = 1
        sourceheight = rheight - rheight * (random.randint(1, 70) / 100)
        pos_src = np.array([[rwidth * random.random(),rlength * random.random(),sourceheight]])
        spkr_pattern = "omni"
        orV_src = None
      
    #print(room_sz, pos_rcv, pos_src)
    
    beta = gpuRIR.beta_SabineEstimation(room_sz, T60, abs_weights=abs_weights) # Reflection coefficients
    Tdiff= gpuRIR.att2t_SabineEstimator(att_diff, T60) # Time to start the diffuse reverberation model [s]
    Tmax = gpuRIR.att2t_SabineEstimator(att_max, T60)	 # Time to stop the simulation [s]
    nb_img = gpuRIR.t2n( Tdiff, room_sz )	# Number of image sources in each dimension
    RIRs = gpuRIR.simulateRIR(room_sz, beta, pos_src, pos_rcv, nb_img, Tmax, fs, Tdiff=Tdiff, orV_rcv=orV_rcv, orV_src=orV_src, mic_pattern=mic_pattern, spkr_pattern=spkr_pattern) 
      
    sample_rate_audio, audio_data = wavfile.read('/tmp/noise.wav')
    audio_data = audio_data.astype(np.float64)
    rir_data = RIRs.astype(np.float64)
    #print(RIRs.shape, audio_data.shape)
  
    if np.max(np.abs(rir_data)) != 0:
        # Normalize the RIR    
        rir_data /= np.max(np.abs(rir_data))
        # Convolve the audio with the RIR
        convolved_audio = fftconvolve(audio_data, rir_data[0][0])
        # Normalize the convolved audio to prevent clipping
        convolved_audio /= np.max(np.abs(convolved_audio))
        # Convert back to 16-bit integer format
        convolved_audio_int = (convolved_audio * 32767).astype(np.int16)
        # Save the new file
        wavfile.write('/tmp/noise.wav', sample_rate_audio, convolved_audio_int)
          

        
    tfm2.clear_effects()
    tfm2.trim(0.1, target_length + 0.1)
    tfm2.norm(-0.1)
    #print(random.random())
    silent_lvl = silent_vol * random.random()
    if silent_percent > random.random():
      tfm2.vol(silent_lvl)
      str_effect = str_effect + "-sil"
      #print(silent_lvl, "Silent lvl")
    else:
      noise_lvl = 1.0 - ((1.0 - noise_vol)  * random.random())
      str_effect = str_effect + "-lou"
      #print(noise_lvl, "Noise lvl")
      tfm2.vol(noise_lvl)
    
    out = os.path.splitext(noise_wav)[0].replace(" ", "") + '-v' + str(version) + str_effect + '.wav'
    out = dest_dir + "/" + shortuuid.uuid() + "-" + os.path.basename(out)
    tfm2.build_file('/tmp/noise.wav', out)
    print(out)
    
def main_body():
  parser = argparse.ArgumentParser()
  parser.add_argument('--dest_dir', default='./dest', help='dest dir location')
  parser.add_argument('--target_qty', type=int, default=4000, help='Final qty of augmented audio files')
  parser.add_argument('--target_length', type=float, default=1.0, help='Target length of audio files to be trimmed to (s)')
  parser.add_argument('--debug', help='debug effect settings to cli', action="store_true")
  parser.add_argument('--noise_dir', default='./noise', help='noise dir location')
  parser.add_argument('--noise_vol', type=float, default=0.9, help='Min Vol of noise foreground (0.9)')
  parser.add_argument('--silent_percent', type=float, default=0.1, help='Percent silent noise to (0.1)')
  parser.add_argument('--silent_vol', type=float, default=0.3, help='Silent noise vol (0.3)')
  args = parser.parse_args()
  
  augment(args.dest_dir, args.target_qty, args.target_length, args.debug, args.noise_dir, args.noise_vol, args.silent_percent, args.silent_vol)
    
if __name__ == '__main__':
  main_body()

