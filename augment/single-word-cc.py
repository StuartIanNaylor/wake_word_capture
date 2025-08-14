import shortuuid
import glob
from pathlib import Path
import os
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

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
gpt_cond_len = 6
gpt_cond_chunk_len = 6

voices = glob.glob('voices/**/*.wav', recursive=True)
#print(voices)
text1 = "computer "
text1_dir = "./computer"
os.mkdir(text1_dir)
text2 = "jacqueline "
text2_dir = "./jacqueline"
os.mkdir(text2_dir)
text3 = "gregory "
text3_dir = "./gregory"
os.mkdir(text3_dir)
text4 = "felicity "
text4_dir = "./felicity"
os.mkdir(text4_dir)
text5 = "maximus "
text5_dir = "./maximus"
os.mkdir(text5_dir)

for language in languages:
    os.mkdir(text1_dir + "/" + language)
    os.mkdir(text2_dir + "/" + language)
    os.mkdir(text3_dir + "/" + language)
    os.mkdir(text4_dir + "/" + language)
    os.mkdir(text5_dir + "/" + language)

    
for voice in voices:
    print("1. Clone the voice from " + voice)
    gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=[voice],
      max_ref_length = max_ref_length,
      gpt_cond_len = gpt_cond_len,
      gpt_cond_chunk_len = gpt_cond_chunk_len,
      )    



    for language in languages:
        text1 = "computer "
        text2 = "jacqueline "
        text3 = "gregory "
        text4 = "felicity "
        text5 = "maximus "
        
        if language == "fr":
            text1 = "computeur "
        if language == "hu":
            text1 = "komputer "
        if language == "pl":
            text1 = "komputer "
        if language == "pt":
            text1 = "kõmputa "
        if language == "ru":
            text1 = "компьютер "
        if language == "ja":
            text1 = "コンピューター "
        if language == "cs":
            text1 = "komputer "
        if language == "nl":
            text1 = "kompyuter "
        if language == "de":
            text1 = "komputer "
        if language == "tr":
            text1 = "kompyuter "
            
            
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
        file_path= text1_dir + "/" + language + "/" + shortuuid.uuid() + "-cc-" + language + '-' + Path(voice).stem + ".wav"
        torchaudio.save(file_path, torch.tensor(out["wav"]).unsqueeze(0), 24000)

        print("Inference..." + text2 + " with voice " + Path(voice).stem + " " + language)
        out = model.inference(
           text2,
           language,
           gpt_cond_latent,
           speaker_embedding,
           temperature = temperature,
           length_penalty = length_penalty,
           repetition_penalty = repetition_penalty,
           top_k = top_k,
           top_p = top_p,
           )
        file_path= text2_dir + "/" + language + "/" + shortuuid.uuid() + "-cc-" + language + '-' + Path(voice).stem + ".wav"
        torchaudio.save(file_path, torch.tensor(out["wav"]).unsqueeze(0), 24000)
        
        print("Inference..." + text3 + " with voice " + Path(voice).stem + " " + language)
        out = model.inference(
           text3,
           language,
           gpt_cond_latent,
           speaker_embedding,
           temperature = temperature,
           length_penalty = length_penalty,
           repetition_penalty = repetition_penalty,
           top_k = top_k,
           top_p = top_p,
           )
        file_path= text3_dir + "/" + language + "/" + shortuuid.uuid() + "-cc-" + language + '-' + Path(voice).stem + ".wav"
        torchaudio.save(file_path, torch.tensor(out["wav"]).unsqueeze(0), 24000)
        
        print("Inference..." + text4 + " with voice " + Path(voice).stem + " " + language)
        out = model.inference(
           text4,
           language,
           gpt_cond_latent,
           speaker_embedding,
           temperature = temperature,
           length_penalty = length_penalty,
           repetition_penalty = repetition_penalty,
           top_k = top_k,
           top_p = top_p,
           )
        file_path= text4_dir + "/" + language + "/" + shortuuid.uuid() + "-cc-" + language + '-' + Path(voice).stem + ".wav"
        torchaudio.save(file_path, torch.tensor(out["wav"]).unsqueeze(0), 24000)
        
        print("Inference..." + text5 + " with voice " + Path(voice).stem + " " + language)
        out = model.inference(
           text5,
           language,
           gpt_cond_latent,
           speaker_embedding,
           temperature = temperature,
           length_penalty = length_penalty,
           repetition_penalty = repetition_penalty,
           top_k = top_k,
           top_p = top_p,
           )
        file_path= text5_dir + "/" + language + "/" + shortuuid.uuid() + "-" + language + '-' + Path(voice).stem + ".wav"
        torchaudio.save(file_path, torch.tensor(out["wav"]).unsqueeze(0), 24000)                    
