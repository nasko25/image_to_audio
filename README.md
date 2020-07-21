# image_to_audio
This project is a webapp that converts text from an image to an audio file with a TTS generated voice. The website is based on two python scripts that firstly extract any text in the uploaded image and then use a google api to convert the text to audio. The generated audio file is then sent back to the client.
    
If the client uploads more than one photo of text, the server will combine the text from all images and will create a single audio file. 

## How to run the project
If you want to try it, you can either visit https://imagetoaudio.com/ or clone the repository and host your own server.
    
If you decide to host your own server, you can run 
'''bash
php -S localhost:8080
'''
and then open `localhost:8080` in your browser (which is not recommended; only use for testing).

If you want to use the Google TTS, you need to create a google account and generate a token to use their api (it is free). Then, you have to add the path to the token in the `text_to_audio.py` file.
    
If you want to use Mozilla TTS, the set up is a bit harder. [Here](https://colab.research.google.com/drive/1u_16ZzHjKYFn1HNVuA4Qf_i2MMFB9olY) is a link to the tutorial I used. Most of the code I used to initilize the TTS was from this tutorial.
    There are more tutorials in the [Github page of Mozilla TTS](https://github.com/mozilla/TTS).

## Libraries
In order to try to fix a poorly taken photo, the website allows users to specify that the photo is not optimal, and then the script will try to dewarp the images using an image processing project from https://github.com/mzucker/page_dewarp.

Since it is written in `python2`, I have been planning to try to rewrite it to `python3` in the near future.
