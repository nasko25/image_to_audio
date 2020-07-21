#! /usr/bin/env python

from google.cloud import texttospeech
from pydub import AudioSegment
import sys
import subprocess
import os

# TODO: maybe use an open source project instead of googleTTS; https://github.com/mozilla/TTS
class ConvertTextToAudio:
    def __init__(self, text, expected_output_audio_format, file_name):
        self.client = texttospeech.TextToSpeechClient()

        self.user_input = texttospeech.types.SynthesisInput(text=str(text))

        self.voice_preferences = texttospeech.types.VoiceSelectionParams(
                language_code = "en-US",
                name = "en-US-Wavenet-B", # or other?
                ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE) # maybe ask the user?

        if expected_output_audio_format == ".wav"  or expected_output_audio_format == ".flac" or expected_output_audio_format == ".aiff" or expected_output_audio_format == ".m4a":
            self.audio_config = texttospeech.types.AudioConfig(
                    audio_encoding = texttospeech.enums.AudioEncoding.LINEAR16)
        else: # expected_output_audio_format == ".mp3 or other
            self.audio_config = texttospeech.types.AudioConfig(
                    audio_encoding = texttospeech.enums.AudioEncoding.MP3) # This should also be the default option if none on the ifs are satisfied

        response = self.client.synthesize_speech(self.user_input, self.voice_preferences, self.audio_config)

        if expected_output_audio_format == ".mp3" or expected_output_audio_format != ".wav" and expected_output_audio_format != ".flac" and expected_output_audio_format != ".aiff" and expected_output_audio_format != ".m4a":
            self.expected_output_audio_format = ".mp3"
        else:
            self.expected_output_audio_format = ".wav"

        with open((file_name + "_audio" + self.expected_output_audio_format), "wb") as out:
            out.write(response.audio_content)
            # print("Audio content written to ", file_name, "_audio", self.expected_output_audio_format, sep="")

        if expected_output_audio_format == ".flac" or expected_output_audio_format == ".aiff":
            old_format = AudsplitioSegment.from_wav(file_name + "_audio" + self.expected_output_audio_format)
            old_format.export(file_name + "_audio" + expected_output_audio_format, format = expected_output_audio_format[1:])
            # remove the wav file
            subprocess.run(["rm", file_name + "_audio" + self.expected_output_audio_format])

        elif expected_output_audio_format == ".m4a":
            p = subprocess.Popen(["ffmpeg", "-i", file_name + "_audio" + self.expected_output_audio_format, "-c:a", "aac", "-b:a", "128k", file_name + "_audio" + expected_output_audio_format], stdout=subprocess.DEVNULL, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
            p.communicate('y'.encode())   # it may ask to override the file
            p.wait()    # wait for it to finish
            subprocess.run(["rm", file_name + "_audio" + self.expected_output_audio_format])


        print(file_name + "_audio" + expected_output_audio_format, end = "")

# ctta_test = ConvertTextToAudio(text = "Hello || This is |||| a test ... 1234!.", expected_output_audio_format = ".flac", file_name = "cccc")
# ConvertTextToAudio(text = "get from a file", expected_output_audio_format = "at the beginning of the file", file_name = "at the beginning of the file")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/path/to/google_credentials.json"

with open(sys.argv[2], 'r') as f:
    ConvertTextToAudio(text = f.read(), expected_output_audio_format = sys.argv[1], file_name = sys.argv[2].split(".")[0])

# TODO remove images after making the txt file. And add script to delete files after 24 hours.
