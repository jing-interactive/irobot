#!/usr/bin/env python3
'''
main.py
'''

# NOTE: this example requires PyAudio because it uses the Microphone class

import argparse
import speech_recognition as sr
from pythonosc import udp_client

import io, os, subprocess, wave, aifc, math, audioop
import collections, threading
import platform, stat
import json, hashlib, hmac, time, base64, random, uuid
import tempfile, shutil

try: # attempt to use the Python 2 modules
    from urllib import urlencode
    from urllib2 import Request, urlopen, URLError, HTTPError
except ImportError: # use the Python 3 modules
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError
    import requests

class MyRecognizer(sr.Recognizer):
    # Baidu Speech Recognition API-Decalogue    
    # From https://github.com/Uberi/speech_recognition/pull/170/commits/8058cef1bb5f7c1a0fdc89e527b26a7c81de03aa
    def recognize_baidu(self, audio_data, *, language = "zh", key = None, secret_key = None, show_all = False):
        """
        Performs speech recognition on ``audio_data`` (an ``AudioData`` instance), using the Baidu Speech Recognition API.
        The Baidu Speech Recognition API key is specified by ``key``. If not specified, it uses a generic key that works out of the box. This should generally be used for personal or testing purposes only, as it **may be revoked by Baidu at any time**.
        百度语音识别接口支持 POST 方式
        目前 API 仅支持整段语音识别的模式，即需要上传整段语音进行识别
        语音数据上传方式有两种：隐示发送和显示发送
        原始语音的录音格式目前只支持评测 8k/16k 采样率 16bit 位深的单声道语音
        压缩格式支持：pcm（不压缩）、wav、opus、speex、amr、x-flac
        系统支持语言种类：中文（zh）、粤语（ct）、英文（en）
        正式地址：http://vop.baidu.com/server_api
        Returns the most likely transcription if ``show_all`` is false (the default). Otherwise, returns the raw API response as a JSON dictionary.
        Raises a ``speech_recognition.UnknownValueError`` exception if the speech is unintelligible. Raises a ``speech_recognition.RequestError`` exception if the key isn't valid, the quota for the key is maxed out, or there is no internet connection.
        """
        assert isinstance(audio_data, sr.AudioData), "`audio_data` must be audio data"
        assert key is None or isinstance(key, str), "`key` must be `None` or a string"
        assert secret_key is None or isinstance(secret_key, str), "`secret_key` must be `None` or a string"
        # Using Rain's default keys of baidu asr api
        if key is None: key = "QrhsINLcc3Io6w048Ia8kcjS"
        if secret_key is None: secret_key = "e414b3ccb7d51fef12f297ffea9ec41d"
        access_token = get_token_baidu(key, secret_key)
        mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
        
        flac_data, sample_rate = audio_data.get_flac_data(), audio_data.sample_rate

        url_post_base = "http://vop.baidu.com/server_api"
        data = {
                "format": "x-flac",
                "lan": language,
                "token": access_token,
                "len": len(flac_data),
                "rate": sample_rate,
                "speech": base64.b64encode(flac_data).decode('UTF-8'),
                "cuid": mac_address,
                "channel": 1,
                }
        json_data = json.dumps(data).encode('UTF-8')
        headers = {"Content-Type": "application/json", "Content-Length": len(json_data)}
        # Obtain audio transcription results
        try:
            response = requests.post(url_post_base, data=json.dumps(data), headers=headers)
        except HTTPError as e:
            raise RequestError("recognition request failed: {0}".format(getattr(e, "reason", "status {0}".format(e.code)))) 
        except URLError as e:
            raise RequestError("recognition connection failed: {0}".format(getattr(e, "reason", "status {0}".format(e.code))))
            
        if int(response.json()['err_no']) != 0:
            return 'err_msg'
        else:
            results = response.json()['result'][0].split("，")
            for item in results:
                if item != "":
                    return item
            return 'err_msg'            

# Get token from baidu
def get_token_baidu(app_key, secret_key):
    url_get_base = "https://openapi.baidu.com/oauth/2.0/token"
    url = url_get_base + "?grant_type=client_credentials" + "&client_id=" + app_key + "&client_secret=" + secret_key
    response = urlopen(url)
    response_text = response.read().decode('UTF-8')
    json_result = json.loads(response_text)
    return json_result['access_token']

def main():
    '''
    main()
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=3000,
                        help="The port the OSC server is listening on")
    parser.add_argument("--filename", default="./words.txt",
                        help="The filename that wil contain the recognized words.")
    parser.add_argument("--back_volume", type=int, default=-1,
                        help="Background volume.")    
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    rec = MyRecognizer()
    mic = sr.Microphone()

    try:
        if args.back_volume == -1:
            print("A moment of silence, please...")
            with mic as source:
                rec.adjust_for_ambient_noise(source)
        else:
            rec.energy_threshold = args.back_volume

        print("Set minimum energy threshold to {}".format(rec.energy_threshold))
        while True:
            print("Say something!")
            with mic as source:
                audio = rec.listen(source)
            print("Got it! Now to recognize it...")
            try:
                style = "sphinx"
                if style == "google":
                    value = rec.recognize_google(audio)
                elif style == "bing":
                    value = rec.recognize_bing(audio, key="0211831985124fdbb41fe2161bc1cd10", language="zh-CN")
                elif style == "baidu":
                    value = rec.recognize_baidu(audio, key="KS7NnNQetwOkanR5x92OHVxB", secret_key="7e87ec1ff0c9c8c9bbe99a1115cc2464")
                elif style == "sphinx":
                    value = rec.recognize_sphinx(audio, language="zh-CN")
                else:
                    value = rec.recognize_sphinx(audio)
                
                if value == "":
                    print("Found nothing!")
                    continue
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
