sudo apt-get install tesseract-ocr -y
# Download an image to test tesseract
# wget https://cdn.shopify.com/s/files/1/0438/2233/products/Poe_s_the_Raven_Note_Card.jpg?v=1431888754
# file Poe_s_the_Raven_Note_Card.jpg\?v\=1431888754
# tesseract Poe_s_the_Raven_Note_Card.jpg\?v\=1431888754 raven

pip install gTTS
# Add the path to PATH to use the command line application (gtts-cli)
# PATH=$PATH:/home/pi/.local/bin
# needed to pip3 install gTTS
# gtts-cli 'hello' --output hello.mp3
# python -m SimpleHTTPServer    to host the mp3 file to download it
# gtts-cli -f raven.txt -o raven.mp3
# tr '\n' ' ' < raven.txt
# tr '\n' ' ' < gatsby.txt | awk -F '   +' '{print $2}' | awk -F '  +' '{print $1 " " $2}'
# gtts-cli "`tr '\n' ' ' < gatsby.txt | awk -F '   +' '{print $2}' | awk -F '  +' '{print $1 " " $2}'`" -o raven-formatted.mp3

# need to write a python script that uses the wavenet voice


# add the path to the json with the google credentions to $PATH   FOR EACH SESSION
# export GOOGLE_APPLICATION_CREDENTIALS="/home/pi/image_to_audio/Test-1074eae5bb81.json"

pip install --upgrade google-cloud-texttospeech
# Needed to pip3 install --upgrade google-cloud-texttospeech

# get a page dewarper to help with the OCR
# git clone https://github.com/mzucker/page_dewarp.git
# need to install the required libraries for page_dewarp
# pip install -r requirements.txt
# since there was no version of opencv for the raspberry pi, I downloaded the code for opencv and compiled it with cmake:
# https://docs.opencv.org/3.3.0/d7/d9f/tutorial_linux_install.html
# TODO find a better dewarper
