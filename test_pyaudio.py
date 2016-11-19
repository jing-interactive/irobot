#!/usr/bin/env python
import pyaudio
import wave
 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 512
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "ceshi-ceshi-%d.wav"
 
audio = pyaudio.PyAudio()
 
for n in range(0, 5):
    filename = WAVE_OUTPUT_FILENAME % (n)

    # start Recording
    print "recording...", filename
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    # stop Recording
    stream.stop_stream()
    stream.close()

    print "finished recording", filename

    waveFile = wave.open(filename, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

audio.terminate()
