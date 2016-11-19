# irobot
A smart rasperry pi (Python 2.x)

## Steps for Linux

* sudo apt-get install python-dev
* sudo apt-get install portaudio19-dev
* sudo pip install PyAudio
* sudo apt-get install mpg123
* sudo apt-get install flac
* pip install python-osc

http://stackoverflow.com/questions/39302974/how-to-capture-audio-in-raspberry-pi-using-pyaudio-python-module-without-overflo

http://stackoverflow.com/questions/10733903/pyaudio-input-overflowed/

###WTF! MUST RUN!###
* jackd -d dummy

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

## Steps for macOS

* sudo apt-get install python-dev
* brew install portaudio
* pip install PyAudio
* brew install mpg123
* brew install flac

## Steps for Windows w/ Python2

* pip install PyAudio

## Steps for Windows w/ conda + Python3

* conda create -n python2 python=2
* activate python2
* pip install PyAudio
