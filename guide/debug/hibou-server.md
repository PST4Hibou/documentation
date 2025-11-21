# Hibou Server Debug

## GStreamer

You can dynamically enable GStreamer debugging at runtime using the option _**--gst-dbg-level**_. By default, it will be NONE, but you can change it.
This will make GStreamer output additional data. To know the possible values, refer to [GStreamer's documentation](https://gstreamer.freedesktop.org/documentation/tutorials/basic/debugging-tools.html)

## Listening to the Audio

You can use _**AUDIO_PLAYBACK**_ to listen to... well, the audio before it is (pre-)processed to determine the presence of a drone.

## Others, GUI

You can manually enable the followings in _src\.settings_.

| Name                  | Description                                                                       |
|-----------------------|-----------------------------------------------------------------------------------|
| AUDIO_ENERGY_SPECTRUM | Display the audio "energy" over time of all the channels.                         |
| AUDIO_STFT_SPECTRUM   | Display the STFT spectrogram of every all the channels, to see the model's input. |
| AUDIO_RADAR           | Display the deduced position based on the audio "energies".                       |
