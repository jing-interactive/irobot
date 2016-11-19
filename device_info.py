#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pyaudio
import pprint

pp = pprint.PrettyPrinter(indent=4)

audio = pyaudio.PyAudio()
count = audio.get_device_count()
print "audio device: " + str(count)
for i in range(count):
    desc = audio.get_device_info_by_index(i)
    pp.pprint(desc)

for i in range(count):
    desc = audio.get_device_info_by_index(i)
    print "\n\n"
    if "PnP" in desc["name"] or "record" in desc["name"]:
        print "DEVICE: %s  INDEX:  %s  RATE:  %s " %  (desc["name"], i,  int(desc["defaultSampleRate"]))
