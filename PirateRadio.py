#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Pirate Radio
# Author: Wynter Woods (Make Magazine)
# Łukasz Marcińczak 2018-03-24


import re
import sys
import os
import subprocess



music_pipe_r, music_pipe_w = os.pipe()


def main(music_dir, frequency=93.4, repeat_all=0):
	daemonize()
	run_pifm(frequency)
	files = build_file_list(music_dir)
	print(files)
	if repeat_all == 1:
		while(True):
			play_songs(files, frequency)
	else:
		play_songs(files, frequency)


def build_file_list(music_dir):
	file_list = []
	for root, folders, files in os.walk(music_dir):
		folders.sort()
		files.sort()
		for filename in files:
			if re.search(".(aac|mp3|mp2|mp4|wav|flac|m4a|ogg)$", filename) != None: 
				file_list.append(os.path.join(root, filename))
	return file_list

def play_songs(file_list, frequency):
	print("Playing songs to frequency ", str(frequency))
	with open(os.devnull, "w") as dev_null:
		for filename in file_list:
			print("Playing ", filename)
			subprocess.call(["ffmpeg", "-i", filename, "-f", "s16le", "-acodec", "pcm_s16le", "-ac", "1", "-ar", "22050", "-"], stdout=music_pipe_w, stderr=dev_null)	

def daemonize():
	fpid = os.fork()
	if fpid != 0:
		sys.exit()

def run_pifm(frequency):
	with open(os.devnull, "w") as dev_null:
		fm_process = subprocess.Popen(["./pifm", "-", str(frequency)], stdin=music_pipe_r, stdout=dev_null)


if __name__ == "__main__":
	try:
		if len(sys.argv) == 4:
			main(sys.argv[1], sys.argv[2], sys.argv[3])
		elif len(sys.argv) == 3:
			main(sys.argv[1], sys.argv[2])
		elif len(sys.argv) == 2:
			main(sys.argv[1])
		else:
			print("Użycie:")
			print("\t<katalog z muzyką> <częstotliwość u MHz (domyślnie 93.4)> <powtarzaj (domyślnie 0)>\nlub:")
			print("\t<katalog z muzyką> <częstotliwość u MHz (domyślnie 93.4)>\nlub:")
			print("\t<katalog z muzyką>\n\n")
			print("np: sudo ./PirateRadio.py /home/user/mp3 93.4 1\n\n\n")
    
	except KeyboardInterrupt:
		print("\n\nProgram zakończony przez użytkownika.\n")
		s.close()
		sys.exit()

