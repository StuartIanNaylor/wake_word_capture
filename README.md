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

`python3 kws-non-stream-avg.py -l` to list devices.

Just a rough hack but if you look at the recorded .wav on KW hit 'Hey Jarvis' you will find its very constant and always in the middle so the capture window can be decresed to quite a tight fit.
Currently double just to show any large movements

I normally use a streaming model but just did the non stream 1st and will update repo later but included as think MicroWake is also no streaming.
On a Pi Zero you have to use the quant model if strides set to 40
Interesting is that if you say just Hey and drop the sensitivity to 0.1 the quant model will trigger but unquant will not
That is more inaccuracy than I thought quant created...

Maybe because I have always used a running average than actual model output is the secret sauce? But capture should be easy as the capture position is very constant.

Maybe if MicroWakeWord is using few strides and polling slowing and not averaging model output that is why.
The non streaming model sort of sucks to a streaming model as 20ms strides with a streaming model causes considerabilly less load.

I dunno about the numpy.ma but hey as I did have
```
def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n
```
also was doing it over declared strides of 30 before.
I am terrible for hacking and changing and never keeping old and the code is not proposed but to demonstrate in a hour or so you can have something.

Either way with an avg or just 1st prob hit the capture point is very consistant.
I never bothered to create and upload the 1st hit for non-stream as sure it will be the same.
I need to add a delay on the capture point and squeeze in on the 'Hey Jarvis' but that doesn't matter.
If the timing is consistant it means you can.

