# wake_word_capture
TF wake_word_capture

You will have to use tensorflow than TFLite as dunno if flexops has been dropped but its a struggle to find out how to compile the pip package with flex ops.  
used to be easy but latest documentation has be using full TF until I do a model with the MFCC frontend outside of the model.  
I used to like it included in the model and use the flex ops delegate but dunno if that has been dropped its still in the tf.lite method of the full tensorflow package.  

The model expects a AGC feed and many microphone volumes are poor I use vlevel  
https://github.com/radiocicletta/vlevel  
very easy just  
```
make
sudo make install
```
Might need to create the ladspa dir if not exist `sudo mkdir /usr/lib/ladspa/` usually and `sudo apt install libjack-jackd2-dev`
```
pcm.vlevel {
    type ladspa
    slave.pcm "plughw:1";
    path "/usr/lib/ladspa/";
    plugins [{
        label vlevel_stereo
        input {
            controls [ 0.2 0.8 20 ]
        }
    }]
}

0.2 = monitor buffer secs
0.8 = strength
20 = max multiply
```
https://github.com/radiocicletta/vlevel/blob/master/docs/technical.txt goes into the internals if curious  
Really the input should be post filtering of something like https://github.com/SaneBow/PiDTLN  
Still though filtering can attenuate in expects 0.7 to 1 for optimum input tolerance so a 2 stage AGC can be beneficial of running vlevel twice  

use pyenv https://github.com/pyenv/pyenv?tab=readme-ov-file#installation to get python 3.10  
great simple util for changing python version  
```
pyenv install -list
pyenv install 3.10.18
pyenv global 3.10.18
python --version #to test
pyenv global system #to switch back to system python version
pyenv versions #to view installed versions
```
take a while as will compile python 3.10.18 but just me I like the native compile version to be avail under pyenv  
helps if you install https://github.com/StuartIanNaylor/zram-swap-config and increase your dphys swap file to stop a OOM but on a Pizero2 eventually...  
can not remember if you need to install libs  
```
sudo apt install build-essential zlib1g-dev  libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev curl \
autotools-dev autoconf libtool pkg-config cmake python3-setuptools python3-wheel libbz2-dev libreadline-dev libsqlite3-dev liblzma-dev tk-dev \
libportaudio2
```
Likely but any version of TF should run if used with the correct version of numpy the 1. version of numpy was used but latter use the later 2. version  
These instructions are just the same to run and create models via https://github.com/google-research/google-research/tree/1d49f2c0d5506a6e11115726164d42f6b7b7b95a/kws_streaming  
Which I have had problems not being to run much past that commit or anything later than pip install tensorflow==2.11.1 but cloning to that branch works as how we got these models.  
Its a shame as it just creates a hurdle but once you know to checkout that commit and that version of tensorflow than what are now lost in time tf_nightly refernces its a great framework to test basic models.  
The python/tf version and pyenv are only really needed if you want to try creating models

```
git clone https://github.com/StuartIanNaylor/wake_word_capture.git
cd wake_word_capture
python3 -m venv --system-site-packages ./venv
source ./venv/bin/activate
pip3 install --upgrade pip
pip install tensorflow==2.11.0 sounddevice numpy==1.26.4 scipy
```
`conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1'` if your struggling with Cuda is prob easiest  
`python3 kws-stream-avg.py -l` to list devices.  
`python kws-stream-avg.py --help` to show params  
`python kws-stream-avg.py --device 0 --kw_length 1.0 --kw_index 0` for current model and the vlevel pcm is idx 0 (change to whatever `python3 kws-stream-avg.py -l` lists)  
You might get a buffer under run as the full TF package loads just ignore but runtime is much lighter.


Just a rough hack but if you look at the recorded .wav on KW hit 'Computer' you will find its very constant and always in the middle so the capture window can be decresed to quite a tight fit.
Currently double just to show any large movements

I am terrible for slack hacking and changing and never keeping old and the code is not proposed but to demonstrate in a hour or so you can have something.
Make sure you have the correct sound card `aplay - l` test the volume `arecord -D plughw:idx -f S16_LE -r 16000 -c1 -V mono test.wav` to view the VU.
Copy the test.wav and have a look at it in Audacity (or other audio editor) to check you are getting a good level without clipping.
The model is trained with variation gain from 0.65 to -0.1 db but some mics have terrible gain and will cause problems if not setup correctly `alsamixer` F5 to include mic settings

If you want to create your own models
```
mkdir gkws
cd gkws
git clone https://github.com/google-research/google-research.git
cd google-research
git checkout fa08dcc009c73c516400dc32e13147b14196becc
```
instructions are at https://github.com/google-research/google-research/blob/master/kws_streaming/experiments/kws_experiments_quantized_12_labels.md but here is my setup
```
KWS_PATH=$PWD
DATA_PATH=$KWS_PATH/data2
MODELS_PATH=$KWS_PATH/models2
CMD_TRAIN="python -m kws_streaming.train.model_train_eval"
```
for the example crnn-state in this repo examples save this as a file called crnn-state
```
$CMD_TRAIN \
--data_url '' \
--data_dir $DATA_PATH/ \
--train_dir $MODELS_PATH/crnn_state/ \
--split_data 0 \
--wanted_words kw,likekw,notkw,noise \
--mel_upper_edge_hertz 7600 \
--how_many_training_steps 20000,20000,20000,20000 \
--learning_rate 0.001,0.0005,0.0001,0.00002 \
--window_size_ms 40.0 \
--window_stride_ms 20.0 \
--mel_num_bins 40 \
--dct_num_features 20 \
--resample 0.0 \
--alsologtostderr \
--train 1 \
--lr_schedule 'exp' \
--use_spec_augment 1 \
--time_masks_number 2 \
--time_mask_max_size 10 \
--frequency_masks_number 2 \
--frequency_mask_max_size 5 \
--feature_type 'mfcc_op' \
--fft_magnitude_squared 1 \
--return_softmax 1 \
crnn \
--cnn_filters '16,16' \
--cnn_kernel_size '(3,3),(5,3)' \
--cnn_act "'relu','relu'" \
--cnn_dilation_rate '(1,1),(1,1)' \
--cnn_strides '(1,1),(1,1)' \
--gru_units 256 \
--return_sequences 0 \
--dropout1 0.1 \
--units1 '128,256' \
--act1 "'linear','relu'" \
--stateful 1
```
Then after doing the same install of python 3.10
```
pip install tensorflow==2.11.1 numpy==1.26.4 tensorflow_addons tensorflow_model_optimization pydot graphviz absl-py
source crnn-state
```
Likey you will want to change your dataset organisation but the above will let you do your own augmentation
Further instructions https://github.com/google-research/google-research/tree/master/kws_streaming#training-on-custom-data
Medium to large datasets can take 24 hours with a decent machine Cuda and a GTX 2070+
The learning rate starts very small to likely stop any overshoots so all models benchmarked get the optimum model.
this does increase training time that really many could run with bigger LR (learning rates)

Added 2 scripts create_prob_txt.py allow you to output the score of a data dir on a selected trained model index.
Creates a txt file that is useful for quick analysis in a spreadsheet.
Often I just sort keeep the worst ofenders and save to use with the del-prob-csv.py script to delete outliers likely from bad TTS or noise files.
Usually the data dir is of the index but cross runs of how its seen by other classes can be illuminating.

Here is the link to the dataset used for training https://drive.google.com/file/d/1YIF-yQUlldIlMRECZKA_1m__OhzFZA8f/view?usp=sharing

BcResNet models are from https://github.com/Qualcomm-AI-research/bcresnet and likely would be better converted from pytorch to Onnx and then maybe via RkNN or https://github.com/rockchip-linux/rknn-toolkit2 https://github.com/espressif/esp-dl depending on NPU or Esp32 

