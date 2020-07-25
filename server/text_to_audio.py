#! /usr/bin/env python3

import sys
import os

from google.cloud import texttospeech
from pydub import AudioSegment

import subprocess

import io

def disable_stdout():
    saved_stdout = sys.stdout

    null_fd = open(os.devnull, 'w')
    sys.stdout = null_fd

    return saved_stdout, null_fd

    # # open 2 fds
    # null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
    # # save the current file descriptors
    # save = os.dup(1), os.dup(2)
    # # put /dev/null fds on 1 and 2
    # os.dup2(null_fds[0], 1)
    # os.dup2(null_fds[1], 2)
    # return save, null_fds

def enable_stdout(saved_stdout, null_fd):
    # restore stdout and stderr file descriptors
    sys.stdout = saved_stdout
    null_fd.close()

    # print(save)
    # os.dup2(save[0], 1)
    # os.dup2(save[1], 2)
    # # close the temporary fds
    # os.close(null_fds[0])
    # os.close(null_fds[1])


import re

import pysbd

import torch
import time

from TTS.tts.utils.generic_utils import setup_model
from TTS.utils.io import load_config
from TTS.tts.utils.text import make_symbols, phonemes, symbols
from TTS.utils.audio import AudioProcessor
from TTS.tts.utils.synthesis import *

from TTS.vocoder.utils.generic_utils import setup_generator

from scipy.io import wavfile

DEBUG = True

if not DEBUG:
    saved_stdout, null_fd = disable_stdout()

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

        if not DEBUG:
            enable_stdout(saved_stdout, null_fd)
        print(file_name + "_audio" + expected_output_audio_format, end = "")

# CITATION: https://github.com/mozilla/TTS/blob/72a6ac54c8cfaa407fc64b660248c6a788bdd381/TTS/server/synthesizer.py
class ConvertTextToAudioMozillaTTS:
    # TODO add comments where needed
    def __init__(self, text, expected_output_audio_format, file_name):
        self.seg = pysbd.Segmenter(language="en", clean=True)
        # runtime settings
        use_cuda = False

        # model paths - models and config files are taken from Mozilla TTS's github page
        TTS_MODEL = "/path/to/checkpoint_130000.pth.tar"
        TTS_CONFIG = "server/config/config.json"
        VOCODER_MODEL = "/path/to/checkpoint_1450000.pth.tar"
        VOCODER_CONFIG = "server/config/config_vocoder.json"

        # load configs
        TTS_CONFIG = load_config(TTS_CONFIG)
        VOCODER_CONFIG = load_config(VOCODER_CONFIG)

        # load the audio processor
        ap = AudioProcessor(**TTS_CONFIG.audio)

        # LOAD TTS MODEL
        # multi speaker
        self.speaker_id = None
        self.speakers = []

        global symbols, phonemes

        use_phonemes = TTS_CONFIG.use_phonemes

        if 'characters' in TTS_CONFIG.keys():
            symbols, phonemes = make_symbols(**TTS_CONFIG.characters)

        if use_phonemes:
            num_chars = len(phonemes)
        else:
            num_chars = len(symbols)

        # load the model
        model = setup_model(num_chars, len(self.speakers), TTS_CONFIG)

        # load model state
        cp =  torch.load(TTS_MODEL, map_location=torch.device('cpu'))

        # load the model
        model.load_state_dict(cp['model'])
        if use_cuda:
            model.cuda()
        model.eval()

        model.decoder.max_decoder_steps = 3000

        # set model stepsize
        if 'r' in cp:
            model.decoder.set_r(cp['r'])

        # # LOAD VOCODER MODEL
        self.vocoder_model = setup_generator(VOCODER_CONFIG)
        self.vocoder_model.load_state_dict(torch.load(VOCODER_MODEL, map_location="cpu")["model"])
        self.vocoder_model.remove_weight_norm()
        self.vocoder_model.inference_padding = 0

        # ap_vocoder = AudioProcessor(**VOCODER_CONFIG['audio'])
        if use_cuda:
            self.vocoder_model.cuda()
        self.vocoder_model.eval()

        # TODO: need to train a model?
        wav = self.tts(model, text, TTS_CONFIG, use_cuda, ap, use_gl=False, figures=True)
        print(len(wav.tobytes()))

        wavfile.write(file_name + "_audio.wav", TTS_CONFIG.audio["sample_rate"], wav)


        cmd_args = {
            # if .wav is expected, call ffmpeg to convert it to a more universal version of .wav
            # because the generated wav file is weird and cannot be played with all audio players.
            ".wav" : ["ffmpeg", "-i", file_name + "_audio.wav", file_name + "w_audio.wav"],
            # other supported audio format conversions
            ".flac" : ["ffmpeg", "-i", file_name + "_audio.wav", file_name + "_audio.flac"],
            ".aiff" : ["ffmpeg", "-i", file_name + "_audio.wav", file_name + "_audio.aiff"],
            ".m4a" : ["ffmpeg", "-i", file_name + "_audio.wav", "-c:a", "aac", "-b:a", "128k", file_name + "_audio.m4a"],
                                                            # no video # audio sampling frequency                   # audio channels
            ".mp3" : ["ffmpeg", "-i", file_name + "_audio.wav", "-vn", "-ar", str(TTS_CONFIG.audio["sample_rate"]), "-ac", "2",
                # bit rate/second
                "-b:a", "192k", file_name + "_audio.mp3"]
        }

        if expected_output_audio_format in cmd_args:
            output_audio_format = expected_output_audio_format
        # otherwise the extention is not valid, so .mp3 is used as default
        else:
            output_audio_format = ".mp3"

        p = subprocess.Popen(cmd_args[output_audio_format], stdout=subprocess.DEVNULL, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
        p.communicate('y'.encode()) # it may ask to override the file
        p.wait()  # wait for it to finish

        # remove the original generated wav file
        subprocess.run(["rm", file_name + "_audio.wav"])

        if expected_output_audio_format == ".wav":
            file_name += "w"

        if not DEBUG:
            enable_stdout(saved_stdout, null_fd)
        print(file_name + "_audio" + output_audio_format, end = "")

    # TODO could be better (!. or !!. at the end of sentence breaks the method)
    def split_into_sentences(self, text):
        return self.seg.segment(text)

    def tts(self, model, text, CONFIG, use_cuda, ap, use_gl, figures=True):
        t_1 = time.time()

        wavs = []
        sens = self.split_into_sentences(text)
        print(sens)
        self.speaker_id = id_to_torch(self.speaker_id)
        if self.speaker_id is not None and use_cuda:
            self.speaker_id = self.speaker_id.cuda()

        for sen in sens:
            # preprocess the given text
            inputs = text_to_seqvec(sen, CONFIG)
            inputs = numpy_to_torch(inputs, torch.long, cuda=use_cuda)
            inputs = inputs.unsqueeze(0)
            print(sen, "\n\n")
            # synthesize voice
            try:
                _, postnet_output, _, _ = run_model_torch(model, inputs, CONFIG, False, self.speaker_id, None)
            except:
                print("ERROR")
                continue
            if self.vocoder_model:
                # use native vocoder model
                vocoder_input = postnet_output[0].transpose(0, 1).unsqueeze(0)
                wav = self.vocoder_model.inference(vocoder_input)
                if use_cuda:
                    wav = wav.cpu().numpy()
                else:
                    wav = wav.numpy()
                wav = wav.flatten()
            else:
                # use GL
                if use_cuda:
                    postnet_output = postnet_output[0].cpu()
                else:
                    postnet_output = postnet_output[0]
                postnet_output = postnet_output.numpy()
                wav = inv_spectrogram(postnet_output, ap, CONFIG)

            # trim silence
            wav = trim_silence(wav, ap)

            wavs += list(wav)
            wavs += [0] * 10000

        # out = io.BytesIO()
        # self.save_wav(wavs, out)
        wavs = np.array(wavs)

        # compute stats
        process_time = time.time() - t_1
        audio_time = len(wavs) / CONFIG.audio['sample_rate']
        print(f" > Processing time: {process_time}")
        print(f" > Real-time factor: {process_time / audio_time}")
        return wavs

        waveform, alignment, mel_spec, mel_postnet_spec, stop_tokens, inputs = synthesis(model, text, CONFIG, use_cuda, ap, self.speaker_id, style_wav=None,
                                                                                truncated=False, enable_eos_bos_chars=CONFIG.enable_eos_bos_chars, use_griffin_lim=True)
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

# read the text to convert to speech from file
text = "Hello, I am just checking the audio formats."
# with open(sys.argv[2], 'r') as f:
#     ConvertTextToAudioMozillaTTS(text= f.read(), expected_output_audio_format = sys.argv[1], file_name = sys.argv[2].split(".")[0])
ConvertTextToAudioMozillaTTS(text=text, expected_output_audio_format = ".mp3", file_name = "asdf")
ConvertTextToAudioMozillaTTS(text=text, expected_output_audio_format = ".m4a", file_name = "asdf")
ConvertTextToAudioMozillaTTS(text=text, expected_output_audio_format = ".flac", file_name = "asdf")
ConvertTextToAudioMozillaTTS(text=text, expected_output_audio_format = ".aiff", file_name = "asdf")
ConvertTextToAudioMozillaTTS(text=text, expected_output_audio_format = ".wav", file_name = "asdf")
ConvertTextToAudioMozillaTTS(text=text, expected_output_audio_format = ".flacq", file_name = "not_valid_format")
