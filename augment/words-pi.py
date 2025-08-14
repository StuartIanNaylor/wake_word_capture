#!/usr/bin/env python3

import os
import argparse
import time
import shortuuid
import sherpa_onnx
import soundfile as sf

parser = argparse.ArgumentParser()
parser.add_argument('--csv_name', default='./word-list', help='word last unk3 without extention')
args = parser.parse_args()

words = open(args.csv_name + '.txt', 'r')
os.mkdir(args.csv_name)
          
tts_config = sherpa_onnx.OfflineTtsConfig(
    model=sherpa_onnx.OfflineTtsModelConfig(
        vits=sherpa_onnx.OfflineTtsVitsModelConfig(
            model="./vits-piper-en_US-libritts_r-medium/en_US-libritts_r-medium.onnx",
            lexicon="",
            data_dir="./vits-piper-en_US-libritts_r-medium/espeak-ng-data",
            dict_dir="",
            tokens="./vits-piper-en_US-libritts_r-medium/tokens.txt",
        ),
        matcha=sherpa_onnx.OfflineTtsMatchaModelConfig(
           acoustic_model="",
           vocoder="",
           lexicon="",
           tokens="",
           data_dir="",
           dict_dir="",
        ),
        kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
            model="",
            voices="",
            tokens="",
            data_dir="",
            dict_dir="",
            lexicon="",
        ),
        provider="cuda",
        debug=False,
        num_threads=4,
    ),
    rule_fsts="",
    max_num_sentences=1,
)
    
if not tts_config.validate():
   raise ValueError("Please check your config")
       
print(tts_config)
tts = sherpa_onnx.OfflineTts(tts_config)   

while True:

    for speed in (0.9, 1.0):
        voices = 904
        for speaker in range(voices):
            word = words.readline().strip()
            if not word:
                quit()
            audio = tts.generate(word, sid=speaker, speed=speed)
            if len(audio.samples) == 0:
                print("Error in generating audios. Please read previous error messages.")
                quit()
            filename = "./" + args.csv_name + "/" + shortuuid.uuid() + "-" + word + "-pi-" + str(speed) + "-sid" + str(speaker) + "-us-en.wav"
            print(filename)
            sf.write(
                filename,
                audio.samples,
                samplerate=audio.sample_rate,
                subtype="PCM_16",
            )
                

    

