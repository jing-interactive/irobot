# irobot
A smart rasperry pi (Python 2.x / 3.x)

## Setup in Linux

* sudo apt-get install python-dev
* sudo apt-get install portaudio19-dev
* sudo pip install PyAudio

## Run in Linux
* jackd -d dummy
* python main.py --ip 102.168.1.1 --port 3333

## Setup in Windows

* http://conda.pydata.org/miniconda.html
* pip install PyAudio

## Run in Windows
* python main.py --ip 102.168.1.1 --port 3333

## Setup in macOS

* http://conda.pydata.org/miniconda.html
* brew install portaudio
* pip install PyAudio

## Run in macOS
* python main.py --ip 102.168.1.1 --port 3333

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

