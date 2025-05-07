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
Might need to create the ladspa dir if not exist

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

`python3 kws-non-stream.py -l` to list devices.

Just a rough hack but if you look at the recorded .wav on KW hit 'Hey Jarvis' you will find its very constant and always in the middle so the capture window can be decresed to quite a tight fit.
Currently double just to show any large movements

