# irobot
A smart rasperry pi (Python 2.x / 3.x)

## Setup in Linux

* sudo apt-get install python-dev
* sudo apt-get install portaudio19-dev
* sudo pip install PyAudio -U

## Run in Linux
* jackd -d dummy
* python main.py --ip 192.168.1.123 --port 3333 --filename "D:/words.txt" --back_volume 200

## Setup in Windows

* http://conda.pydata.org/miniconda.html
* pip install PyAudio -U
* pip install PocketSphinx
* https://drive.google.com/uc?id=0Bw_EqP-hnaFNSWdqdm5maWZtTGc&export=download

## Run in Windows
* python main.py --ip 192.168.1.123 --port 3333 --filename "D:/words.txt" --back_volume 200

## Setup in macOS

* http://conda.pydata.org/miniconda.html
* brew install portaudio
* pip install PyAudio -U
* pip install --global-option='build_ext' --global-option='-I/usr/local/include' --global-option='-L/usr/local/lib' pyaudio

## Run in macOS
* python main.py --ip 192.168.1.123 --port 3333 --filename "D:/words.txt" --back_volume 200

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

