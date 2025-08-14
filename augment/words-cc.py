import shortuuid
import glob
from pathlib import Path
import os
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--csv_name', default='./word-list', help='word last unk3 without extention')
args = parser.parse_args()

words = open(args.csv_name + '.csv', 'r')

print("Loading model...")
config = XttsConfig()
path_to_xtts = "/home/stuart/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2"
config.load_json(path_to_xtts + "/config.json")
model = Xtts.init_from_config(config)
model.load_checkpoint(config, checkpoint_dir=path_to_xtts, use_deepspeed=True)
model.cuda()
languages = ('en', 'es', 'fr', 'de', 'it', 'pt', 'pl', 'tr', 'ru', 'nl', 'cs', 'ar', 'zh-cn', 'hu', 'ja')
print(languages)

temperature = 0.75
length_penalty = 1.0
repetition_penalty = 10.0
top_k = 50
top_p = 0.85
max_ref_length = 30
gpt_cond_len = 12
gpt_cond_chunk_len = 6

voices = glob.glob('voices/**/*.wav', recursive=True)
#print(voices)

text1_dir = "./" + args.csv_name

while True:
  word = words.readline()
  if not word:
    break
  text1 = word.strip()
     
  for voice in voices:
      print("1. Clone the voice from " + voice)
      gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=[voice],
        max_ref_length = max_ref_length,
        gpt_cond_len = gpt_cond_len,
        gpt_cond_chunk_len = gpt_cond_chunk_len,
        )    

      for language in languages:                  
          print("Inference..." + text1 + " with voice " + Path(voice).stem + " " + language)
          out = model.inference(
             text1,
             language,
             gpt_cond_latent,
             speaker_embedding,
             temperature = temperature,
             length_penalty = length_penalty,
             repetition_penalty = repetition_penalty,
             top_k = top_k,
             top_p = top_p,
             )
          file_path= text1_dir + "/" + shortuuid.uuid() + "-cc-" + language + '-' + Path(voice).stem + ".wav"
          torchaudio.save(file_path, torch.tensor(out["wav"]).unsqueeze(0), 24000)


