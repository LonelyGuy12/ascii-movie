import asyncio
import cv2
import imgkit
import shutil
import ascii_magic
from ascii_magic import AsciiArt
import os
import sys
from moviepy import *
from moviepy.editor import VideoFileClip
import numpy as np
import moviepy.editor as mp
#import admin
from datetime import timedelta

'''
if not admin.isUserAdmin():
        admin.runAsAdmin()
'''

audio_from_video = mp.VideoFileClip("./video.mp4")
vidObj = cv2.VideoCapture("./video.mp4")
print("Video Captured Successfully")
audio_from_video.audio.write_audiofile("./audio.mp3")
print("Audio Captured Successfully")

count = 0
flag = 1
while flag:
    flag, image = vidObj.read()
    try:
        cv2.imwrite(f"./images/frame{count}.jpg", image)
    except:
        break
    count += 1

for i in range(count):
    s = f"./images/frame{str(i)}.jpg"
    output = AsciiArt.from_image(
        s
    )
    output.to_html_file(f"./html/frame{str(i)}.html",
        additional_styles='background: #222;',
        columns = 250,
        width_ratio = 2,)

path = "./wkhtmltoimage.exe"
config = imgkit.config(wkhtmltoimage=path)
for i in range(count):
    imgkit.from_file(f"./html/frame{str(i)}.html", f"./ascii/frame{str(i)}.jpg", config=config)

frame = cv2.imread("./ascii/frame0.jpg")
ih, iw, il = frame.shape
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter('./asciivideo.mp4', fourcc, 60, (iw, ih))

for i in range(count):
    image = f"./ascii/frame{str(i)}.jpg"
    data = cv2.imread(image)
    video.write(data)

cv2.destroyAllWindows()
video.release()

audio = mp.AudioFileClip("./audio.mp3")
video = mp.VideoFileClip("./asciivideo.mp4")

final = video.set_audio(audio)

final.write_videofile("./output.mp4")

shutil.rmtree("./images", ignore_errors=True)
print("Images Cleaned Successfully")
os.mkdir("./images")
print("Images remade Successfully")
shutil.rmtree("./html", ignore_errors=True)
print("HTML Cleaned Successfully")
os.mkdir("./html")
print("HTML remade Successfully")
shutil.rmtree("./ascii", ignore_errors=True)
print("Ascii Images Cleaned Successfully")
os.mkdir("./ascii")
print("Ascii Images remade Successfully")

asyncio.sleep(2)
print("Over and out!")
