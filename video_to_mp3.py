#converts videos to mp3
import os
import subprocess #python module used to run external commands like ffmpeg

files = os.listdir("videos")

for file in files:

    #now i want to print tutorial number and file name 

    #examples of the filenames
    /* "Lecture 1 ｜ Python Basics #001.mp4",
        "Lecture 2 ｜ Variables #002.mp4",
        "Lecture 3 ｜ Loops #003.mp4" */

    tutorial_number = file.split(" #")[1] #1st number of position

    file_name = file.split(" ｜ ")[0]#0th nuber of position
    print(tutorial_number,file_name)

    #this is for convert all the mp4(videos) file into audio(mp3) files.
    #subprocess.run(input,output)
    subprocess.run(["ffmpeg", "-i" ,f"videos/{file}", f"audios/{tutorial_number}_{file_name}.mp3" ])
