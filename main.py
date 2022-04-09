import cv2
import imgkit
import ascii_magic
import os
import sys
from moviepy.editor import VideoFileClip
import numpy as np
import moviepy.editor as mp
import admin
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
    output = ascii_magic.from_image_file(
        s,
        columns = 250,
        width_ratio = 2,
        mode = ascii_magic.Modes.HTML
    )
    ascii_magic.to_html_file(f"./html/frame{str(i)}.html", output, additional_styles='background: #222;')

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
