#!/usr/bin/env python3

import os
import argparse
import time
import shortuuid
import sherpa_onnx
import soundfile as sf

def main():

    texts = ("computer ", "jacqueline ", "gregory ", "felicity ", "maximus ")
    for text in texts:
        text_dir = "./" + text.strip() + "-kk"
        os.mkdir(text_dir)
            
    for version in ("./kokoro-multi-lang-v1_0", "./kokoro-multi-lang-v1_1"):
        voices = 53
        v = "1"
        if version == "./kokoro-multi-lang-v1_1":
            voices = 102
            v = "1_1"
            
        tts_config = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
                vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                    model="",
                    lexicon="",
                    data_dir="",
                    dict_dir="",
                    tokens="",
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
                    model=version + "/model.onnx",
                    voices=version + "/voices.bin",
                    tokens=version + "/tokens.txt",
                    data_dir=version + "/espeak-ng-data",
                    dict_dir=version + "/dict",
                    lexicon=version + "/lexicon-us-en.txt",
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
        for speed in (0.95, 1.05):
            for speaker in range(voices):
                for text in texts:
                    audio = tts.generate(text, sid=speaker, speed=speed)

                    if len(audio.samples) == 0:
                        print("Error in generating audios. Please read previous error messages.")
                        return

                    filename = "./" + text.strip() + "-kk/" + shortuuid.uuid() + "-kk" + v + "-" + str(speed) + "-sid" + str(speaker) + "-us-en.wav"
                    print(filename)
                    sf.write(
                        filename,
                        audio.samples,
                        samplerate=audio.sample_rate,
                        subtype="PCM_16",
                    )
        
        tts_config = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
                vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                    model="",
                    lexicon="",
                    data_dir="",
                    dict_dir="",
                    tokens="",
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
                    model=version + "/model.onnx",
                    voices=version + "/voices.bin",
                    tokens=version + "/tokens.txt",
                    data_dir=version + "/espeak-ng-data",
                    dict_dir=version + "/dict",
                    lexicon=version + "/lexicon-gb-en.txt",
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

        for speed in (0.95, 1.05):
            for speaker in range(voices):
                for text in texts:
                    audio = tts.generate(text, sid=speaker, speed=speed)

                    if len(audio.samples) == 0:
                        print("Error in generating audios. Please read previous error messages.")
                        return

                    filename = "./" + text.strip() + "-kk/" + shortuuid.uuid() + "-kk" + v + "-" + str(speed) + "-sid" + str(speaker) + "-gb-en.wav"
                    print(filename)
                    sf.write(
                        filename,
                        audio.samples,
                        samplerate=audio.sample_rate,
                        subtype="PCM_16",
                    )
                
if __name__ == "__main__":
    main()
    

