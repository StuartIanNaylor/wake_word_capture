On a PiZero2 you can feed the KWS with https://github.com/SaneBow/PiDTLN using the NS model that actually does a really good job.
The output of the feed to vlevel to boost again as the model expects a normalised AGC input.
```
defaults.pcm.rate_converter "samplerate"

pcm.fixed_rate_cap {
    type plug
    slave {
        pcm "hw:2,0"  # Replace with your card and device (e.g., "hw:1,0")
        rate 16000    # Example: Set the sample rate to 44.1 kHz
        format S16_LE #  Use the appropriate format (e.g., S16_LE, S32_LE)
        channels 2
    }
  route_policy sum
}

pcm.vlevel {
    type ladspa
    slave {
   pcm "plughw:1,1"
   }
    path "/usr/lib/ladspa/";
    plugins [{
        label vlevel_mono
        input {
            controls [ 0.25 0.8 10 ]
        }
    }]
}

pcm.agc_mono {
    type plug
    route_policy sum
    slave {
        pcm "plug:vlevel"  
        rate 16000    
        format S16_LE 
        channels 2
    }
}
```
An example /etc/asound.conf.
You pick the input to DTLN such as fixed_rate_cap and output DTLN to one side of a loopback
Place the vlevel ladspa pluging on the other side of the loopback and use agc_mono for the input to the wakeword.
Instructions how are on the https://github.com/SaneBow/PiDTLN page
