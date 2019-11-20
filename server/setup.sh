sudo apt-get install tesseract-ocr -y
# Download an image to test tesseract
# wget https://cdn.shopify.com/s/files/1/0438/2233/products/Poe_s_the_Raven_Note_Card.jpg?v=1431888754
# file Poe_s_the_Raven_Note_Card.jpg\?v\=1431888754
# tesseract Poe_s_the_Raven_Note_Card.jpg\?v\=1431888754 raven

pip install gTTS
# Add the path to PATH to use the command line application (gtts-cli)
# PATH=$PATH:/home/pi/.local/bin
export GOOGLE_APPLICATION_CREDENTIALS="/home/chrome/one/Test-1074eae5bb81.json"
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
# page_dewarper is good enough for now

# to find dpi of an image
# identify -format '%x,%y\n' image.jpg 
# to change dpi of an image
# convert -units PixelsPerInch image.jpg -density 300 image300.jpg
# they both need
# sudo apt-get install -y imagemagick

# TODO make a script that dewarps an image, uses tesseract on it, and uses gTTS. Also, make sure the web interface tells the user to open the page as much as possible so that there is as little as possible text warping.
# Then, connect the server and client. (after testing extensively)

sudo pip install pytesseract 

# change the default upload_file_size_limit in php.ini to at least 5M.

# NOT NEEDED 
# sudo apt-get install ffmpeg
# sudo pip install --upgrade AudioConverter
# I had to sudo apt-get remove python3-pip; sudo apt-get install python3-pip
# and then do sudo pip3 install --upgrade AudioConverter

sudo pip3 install pydub

# need pillow for the image processing in page_dewarp
sudo pip install Pillow

# needed for audio conversions
sudo apt-get install ffmpeg
