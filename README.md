# irobot
A smart rasperry pi (Python 2.x / 3.x)

## Steps for Linux

* sudo apt-get install python-dev
* sudo apt-get install portaudio19-dev
* sudo pip install PyAudio

* jackd -d dummy

## Steps for Windows

* http://conda.pydata.org/miniconda.html
* pip install PyAudio

## Steps for macOS

* http://conda.pydata.org/miniconda.html
* brew install portaudio
* pip install PyAudio

### MISC info ###
http://stackoverflow.com/questions/39302974/how-to-capture-audio-in-raspberry-pi-using-pyaudio-python-module-without-overflo

http://stackoverflow.com/questions/10733903/pyaudio-input-overflowed/
* sudo leafpad /usr/share/alsa/alsa.conf
* cat ~/.asoundrc

### Test mic & speaker
* aplay bell.wav
* ./test_mic.sh
* aplay f1.wav

* arecord -l
* aplay -l
* cat /proc/asound/modules

### Misc tools
* speaker-test
* sudo raspi-config / Advanced / Audio
* alsamixer
* audacity

