#!/usr/bin/env python3
'''
main.py
'''

# NOTE: this example requires PyAudio because it uses the Microphone class

import argparse
import speech_recognition as sr
from pythonosc import udp_client

def main():
    '''
    main()
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=3000,
                        help="The port the OSC server is listening on")
    parser.add_argument("--filename", default="D:/words.txt",
                        help="The filename that wil contain the recognized words.")    
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    rec = sr.Recognizer()
    mic = sr.Microphone()

    try:
        print("A moment of silence, please...")
        with mic as source:
            rec.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(rec.energy_threshold))
        while True:
            print("Say something!")
            with mic as source:
                audio = rec.listen(source)
            print("Got it! Now to recognize it...")
            try:
                # recognize speech using Google Speech Recognition
                # value = r.recognize_google(audio)
                # value = rec.recognize_bing(audio, key="0211831985124fdbb41fe2161bc1cd10", language="zh-CN")
                value = rec.recognize_baidu(audio, key="KS7NnNQetwOkanR5x92OHVxB", secret_key="7e87ec1ff0c9c8c9bbe99a1115cc2464")

                # we need some special handling here to correctly print unicode
                # characters to standard output
                if str is bytes: # this version of Python uses bytes for strings (Python 2)
                    value = u"{}".format(value).encode("utf-8")
                print("You said", value)
                with open(args.filename, 'w', encoding='utf8') as f:
                	f.write(value);
                client.send_message("/say", value)
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
            except sr.RequestError as err:
                print("Uh oh! Couldn't request results from; {0}".format(err))
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
