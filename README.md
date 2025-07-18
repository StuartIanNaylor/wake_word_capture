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
Might need to create the ladspa dir if not exist /usr/lib/ladspa/ usually
```
pcm.vlevel {
    type ladspa
    slave.pcm "plughw:1";
    path "/usr/lib/ladspa/";
    plugins [{
        label vlevel_stereo
        input {
            controls [ 0.2 0.8 10 ]
        }
    }]
}

0.2 = monitor buffer secs
0.8 = strength
10 = max multiply
```

use pyenv https://github.com/pyenv/pyenv?tab=readme-ov-file#installation to get python 3.10
great simple util for changing python version
```
pyenv install -list
pyenv install 3.10.18
pyenv global 3.10.18
python --version #to test
python global system #to switch back to system python version
```
take a while as will compile python 3.10.18 but just me I like the native compile version to be avail
helps if you install https://github.com/StuartIanNaylor/zram-swap-config and increase your dphys swap file to stop a OOM but on a Pizero2 eventually...
can not remember if you need to install libs
```
sudo apt install build-essential zlib1g-dev  libncurses5-dev libgdbm-dev libnss3-dev  libssl-dev libreadline-dev libffi-dev curl
```
Likely but any version of TF should run if used with the correct version of numpy the 1. version of numpy was used but latter use the later 2. version
These instructions are just the same to run and create models via https://github.com/google-research/google-research/tree/1d49f2c0d5506a6e11115726164d42f6b7b7b95a/kws_streaming
Which I have had problems not being to run much past that commit or anything later than pip install tensorflow==2.11.1 but cling to that branch works as how we got these models.
Its a shame as it just creates a hurdle but once you know to checkout that commit and that version of tensorflow than what are now lost in time tf_nightly refernces its a great framework to test basic models.

```
git clone https://github.com/StuartIanNaylor/wake_word_capture.git
cd wake_word_capture
python3 -m venv --system-site-packages ./venv
source ./venv/bin/activate
pip3 install --upgrade pip
```

`python3 kws-non-stream-avg.py -l` to list devices.

Just a rough hack but if you look at the recorded .wav on KW hit 'Computer' you will find its very constant and always in the middle so the capture window can be decresed to quite a tight fit.
Currently double just to show any large movements

I am terrible for round hacking and changing and never keeping old and the code is not proposed but to demonstrate in a hour or so you can have something.

Either way with an avg or just 1st prob hit the capture point is very consistant.
I never bothered to create and upload the 1st hit for non-stream as sure it will be the same.
I need to add a delay on the capture point and squeeze in on the 'Computer' but that doesn't matter.
If the timing is consistant it means you can.

