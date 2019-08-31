#! /usr/bin/env python
# 1 image proccessing
# 2 tesseract

try:
    from PIL import Image
except ImportError:
    import Image

import pytesseract
import cv2
import sys 
import os 

# sys.stdout = open('reached_python.txt', 'a')
print "reached python code; image file name: " , str(sys.argv)
# os.system("touch reached_python")

# The script will be called whenever the user uploads an image to be conveted.
# Firstly, it will spawn a new process/thread, which will create a random value and create a folder with a name that is the random value. If such a folder already exists, the script will save an image proccessed with (page_dewarp and) pytesseract there as a txt file with a random name. 

name = sys.argv[1].partition("/")[2].partition(".")[0]
# print(name)
# exit()
if len(sys.argv) >=3 and sys.argv[2] == "pd":
    os.system("python page_dewarp/page_dewarp.py " + sys.argv[1])
    os.system("mv " + name + "_thresh.png uploads/")
    print(pytesseract.image_to_string(Image.open("uploads/" + name + "_thresh.png")).encode('utf-8').replace("\n", " "))
else:
    print(pytesseract.image_to_string(Image.open(sys.argv[1])).encode('utf-8').replace("\n", " "))


# It could also format the txt file (remove \n).
# If there is a - followed by a space (because the new line was converted to a space) remove the dash and the space (as it most likely is a single word on two lines)
# Maybe also remove the things from the very top and very bottom (like titles/authors and page numbers on a book) (they are usually separated by several new lines)
# Also tell the user to crop the image, so that there is only text from one page at a time; and take as good of a photo as possible.
# Then it will call another script, passing the name of the folder, and the file name (as a path), and will save an audio file with the random name. 
# Then it will somehow send the audio file (either as a POST response or by email).
# Finally, the script will delete the file, wait for a second, and delete the folder and then kill the thread.

# Add an option in the website to turn on page_dewarp if the image needs it.
# Add guide with pictures in the website to show how to take images and crop them.