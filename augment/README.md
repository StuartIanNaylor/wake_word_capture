# wake_word_capture

pip install soundfile shortuuid sox

```
python trim.py --source_dir /media/stuart/data1/coqui-ai-TTS/voices-df --dest_dir /media/stuart/data1/coqui-ai-TTS/voices-trim --start_length 25.0 --end_length 77.0 --tries 5

python trim.py --source_dir /home/stuart/coqui-ai-TTS/computer --dest_dir /home/stuart/coqui-ai-TTS/computer-trim --start_length .7 --end_length 1.0 --tries 5
```

```
python augment.py --source_dir unk2.trim --dest_dir unk2.aug --target_qty 165003 --target_length 1.0 --noise_dir /home/stuart/data2/audio/noise --noise_vol 0.25 --noise_percent 0.8 --min_vol 0.70
```
```
python split.py --source_dir unk2.aug --dest_dir /home/stuart/data2/Linux-data/gkws/data2 --testing_percent 0.03 --validation_percent 0.12  --label unk2
```

