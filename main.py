#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import argparse
import speech_recognition as sr
from pythonosc import dispatcher, osc_server

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
        type=int, default=3000, help="The port to listen on")
    args = parser.parse_args()

    # server = osc_server.ThreadingOSCUDPServer(
    #     (args.ip, args.port), dispatcher)
    # print("Serving on {}".format(server.server_address))
    # server.serve_forever()

    r = sr.Recognizer()
    m = sr.Microphone()

    try:
        print("A moment of silence, please...")
        with m as source: r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(r.energy_threshold))
        while True:
            print("Say something!")
            with m as source: audio = r.listen(source)
            print("Got it! Now to recognize it...")
            try:
                # recognize speech using Google Speech Recognition
                # value = r.recognize_google(audio)
                value = r.recognize_bing(
                    audio, key="0211831985124fdbb41fe2161bc1cd10", language="zh-CN")

                # we need some special handling here to correctly print unicode
                # characters to standard output
                if str is bytes: # this version of Python uses bytes for strings (Python 2)
                    print(u"You said {}".format(value).encode("utf-8"))
                else: # this version of Python uses unicode for strings (Python 3+)
                    print("You said {}".format(value))
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
    except KeyboardInterrupt:
        pass
