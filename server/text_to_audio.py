#! /usr/bin/env python

from google.cloud import texttospeech
import sys

# TODO Set the enviroment variable to the path to the .json with the credentials
    # ...
class ConverTextToAudio: # python syntax?
    def __init__(self, text, expected_output_audio_format, file_name):
        self.client = texttospeech.TextToSpeechClient()

        self.user_input = texttospeech.types.SynthesisInput(text=str(text))

        self.voice_preferences = texttospeech.types.VoiceSelectionParams(
                language_code = "en-US",
                name = "en-US-Wavenet-B", # or other?
                ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE) # maybe ask the user?

        if expected_output_audio_format == ".mp3":
            self.audio_config = texttospeech.types.AudioConfig(
                    audio_encoding = texttospeech.enums.AudioEncoding.MP3) # This should also be the default option if none on the ifs are satisfied
        # elif ...

        response = self.client.synthesize_speech(self.user_input, self.voice_preferences, self.audio_config)

        if expected_output_audio_format != ".mp3" and expected_output_audio_format != ".wav" and expected_output_audio_format != ".aac":
            self.expected_output_audio_format = ".mp3"
        else:
            self.expected_output_audio_format = expected_output_audio_format
        
        with open((file_name + "_audio" + self.expected_output_audio_format), "wb") as out:
            out.write(response.audio_content)
            print("Audio content written to ", file_name, "_audio", self.expected_output_audio_format)

ctta_test = ConverTextToAudio(text = "Hello. I am Special Agent Fox Mulder with the Federal Bureau of Investigation.", expected_output_audio_format = ".mp3", file_name = "aaaa")