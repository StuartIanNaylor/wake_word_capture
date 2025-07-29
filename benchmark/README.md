# benchmark

wget https://www.openslr.org/resources/12/train-clean-100.tar.gz
tar -xvzf train-clean-100.tar.gz
pip install soundfile scipy

`python benchmark_clean.py --libri-dir /LibriSpeech/train-clean-100`

Still trying to work out a way to match the AGC input that should make sure input fits the 0.7 - 1.0 training levels.
Using ALSA would make in realtime sox norm also isn't comparitive as the recordings are long term but have spurious peaks that still means the RMS level is below expected.
Its a good tool still though to see what word and typr of words are creating false positives.
Doing this has prompted me to to create a '2syl' class as 'future' and similar words are obviously closer to 'KW' from results.
Prob could modify the LikeKw classes but now wondering why I never produced a 2syl class.
Under inspection the sylable code is picking up 'future' as 3 sylable so would niether end up in 2syl or the current 'lk_er' view
I am just going to run some updates to fix the database by hand and this is a ToDo and sylable matching.
https://github.com/sloev/spacy-syllables might be a better option than NLTK code used
