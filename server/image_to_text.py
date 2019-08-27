#! /usr/bin/env python
# 1 image proccessing
# 2 tesseract

import pytesseract
import sys 
import os 

sys.stdout = open('reached_python.txt', 'a')
print "reached python code; image file name: " , str(sys.argv)
# os.system("touch reached_python")

# The script will be called whenever the user uploads an image to be conveted.
# Firstly, it will spawn a new process/thread, which will create a random value and create a folder with a name that is the random value. If such a folder already exists, the script will save an image proccessed with page_dewarp and pytesseract there as a txt file with a random name. 
# Then it will call another script, passing the name of the folder, and the file name (as a path), and will save an audio file with the random name. 
# Then it will somehow send the audio file (either as a POST response or by email).
# Finally, the script will delete the file, wait for a second, and delete the folder and then kill the thread.
