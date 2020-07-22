#! /usr/bin/env python3

# from google.cloud import texttospeech
from pydub import AudioSegment
import sys
import subprocess
import os

import torch
import time

from TTS.utils.generic_utils import setup_model
from TTS.utils.io import load_config
from TTS.utils.text.symbols import symbols, phonemes
from TTS.utils.audio import AudioProcessor
from TTS.utils.synthesis import synthesis

from TTS.vocoder.utils.generic_utils import setup_generator

from scipy.io import wavfile

# TODO: maybe use an open source project instead of googleTTS; https://github.com/mozilla/TTS
class ConvertTextToAudioGoogleTTS:
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
        else: # expected_output_audio_format == ".mp3" or other
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
            old_format = AudioSegment.from_wav(file_name + "_audio" + self.expected_output_audio_format)
            old_format.export(file_name + "_audio" + expected_output_audio_format, format = expected_output_audio_format[1:])
            # remove the wav file
            subprocess.run(["rm", file_name + "_audio" + self.expected_output_audio_format])

        elif expected_output_audio_format == ".m4a":
            p = subprocess.Popen(["ffmpeg", "-i", file_name + "_audio" + self.expected_output_audio_format, "-c:a", "aac", "-b:a", "128k", file_name + "_audio" + expected_output_audio_format], stdout=subprocess.DEVNULL, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
            p.communicate('y'.encode())   # it may ask to override the file
            p.wait()    # wait for it to finish
            subprocess.run(["rm", file_name + "_audio" + self.expected_output_audio_format])


        print(file_name + "_audio" + expected_output_audio_format, end = "")

class ConvertTextToAudioMozillaTTS:
    def __init__(self, text, expected_output_audio_format, file_name):
        # runtime settings
        use_cuda = False

        # model paths
        TTS_MODEL = "/path/to/tts_model.pth.tar"
        TTS_CONFIG = "config/config.json"
        VOCODER_MODEL = "/path/to/vocoder_model.pth.tar"
        VOCODER_CONFIG = "config/config_vocoder.json"

        # load configs
        TTS_CONFIG = load_config(TTS_CONFIG)
        VOCODER_CONFIG = load_config(VOCODER_CONFIG)

        # load the audio processor
        ap = AudioProcessor(**TTS_CONFIG.audio)

        # LOAD TTS MODEL
        # multi speaker
        self.speaker_id = None
        self.speakers = []

        # load the model
        num_chars = len(phonemes) if TTS_CONFIG.use_phonemes else len(symbols)
        model = setup_model(num_chars, len(self.speakers), TTS_CONFIG)

        # load model state
        cp =  torch.load(TTS_MODEL, map_location=torch.device('cpu'))

        # load the model
        model.load_state_dict(cp['model'])
        if use_cuda:
            model.cuda()
        model.eval()

        # set model stepsize
        if 'r' in cp:
            model.decoder.set_r(cp['r'])

        # LOAD VOCODER MODEL
        self.vocoder_model = setup_generator(VOCODER_CONFIG)
        self.vocoder_model.load_state_dict(torch.load(VOCODER_MODEL, map_location="cpu")["model"])
        self.vocoder_model.remove_weight_norm()
        self.vocoder_model.inference_padding = 0

        ap_vocoder = AudioProcessor(**VOCODER_CONFIG['audio'])
        if use_cuda:
            self.vocoder_model.cuda()
        self.vocoder_model.eval()

        # TODO: need to train a model
        align, spec, stop_tokens, wav = self.tts(model, text, TTS_CONFIG, use_cuda, ap, use_gl=False, figures=True)

        wavfile.write(file_name + "_audio.wav", TTS_CONFIG.audio["sample_rate"], wav)

        # if it is any of the other supported audio formats
        if expected_output_audio_format == ".flac" or expected_output_audio_format == ".aiff" or expected_output_audio_format == ".mp3":
            old_format = AudioSegment.from_wav(file_name + "_audio.wav")
            old_format.export(file_name + "_audio" + expected_output_audio_format, format = expected_output_audio_format[1:])
            # remove the wav file
            subprocess.run(["rm", file_name + "_audio.wav"])

        elif expected_output_audio_format == ".m4a":
            p = subprocess.Popen(["ffmpeg", "-i", file_name + "_audio.wav", "-c:a", "aac", "-b:a", "128k", file_name + "_audio" + expected_output_audio_format], stdout=subprocess.DEVNULL, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
            p.communicate('y'.encode())   # it may ask to override the file
            p.wait()    # wait for it to finish
            subprocess.run(["rm", file_name + "_audio.wav"])

    def tts(self, model, text, CONFIG, use_cuda, ap, use_gl, figures=True):
        t_1 = time.time()
        waveform, alignment, mel_spec, mel_postnet_spec, stop_tokens, inputs = synthesis(model, text, CONFIG, use_cuda, ap, self.speaker_id, style_wav=None,
                                                                                truncated=False, enable_eos_bos_chars=CONFIG.enable_eos_bos_chars)
        # mel_postnet_spec = ap._denormalize(mel_postnet_spec.T)
        if not use_gl:
            waveform = self.vocoder_model.inference(torch.FloatTensor(mel_postnet_spec.T).unsqueeze(0))
            waveform = waveform.flatten()
        if use_cuda:
            waveform = waveform.cpu()
        waveform = waveform.numpy()
        rtf = (time.time() - t_1) / (len(waveform) / ap.sample_rate)
        tps = (time.time() - t_1) / len(waveform)
        print(waveform.shape)
        print(" > Run-time: {}".format(time.time() - t_1))
        print(" > Real-time factor: {}".format(rtf))
        print(" > Time per step: {}".format(tps))

        return alignment, mel_postnet_spec, stop_tokens, waveform

# ctta_test = ConvertTextToAudioGoogleTTS(text = "Hello || This is |||| a test ... 1234!.", expected_output_audio_format = ".flac", file_name = "cccc")
# ConvertTextToAudioGoogleTTS(text = "get from a file", expected_output_audio_format = "at the beginning of the file", file_name = "at the beginning of the file")

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/path/to/google_credentials.json"

# with open(sys.argv[2], 'r') as f:
#     ConvertTextToAudioGoogleTTS(text = f.read(), expected_output_audio_format = sys.argv[1], file_name = sys.argv[2].split(".")[0])

ConvertTextToAudioMozillaTTS(text= "This is a test sentence. I will copy some text to check the generated speech.\nSmile spoke total few great had never their too. Amongst moments do in arrived at my replied.",
                                expected_output_audio_format = ".m4a", file_name = "asdfasdf")

