import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
 
from tkinter import ttk
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
from pygame import mixer
 
# Root Window contains Status Bar, Left Frame and Right Frame
# LeftFrame contains listbox (playlist)
# RightFrame contains all the control buttons like play, pause, stop, rewind, mute and volume control
 
 
root = tk.ThemedTk()
root.set_theme("arc")         
 
statusbar = ttk.Label(root, text="Welcome to TuneMate", relief=SUNKEN, anchor=W, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)
 
# Create the menubar
menubar = Menu(root)
root.config(menu=menubar)
 
# Create the submenu
subMenu = Menu(menubar, tearoff=0)
 
playlist = []   # contains the full path + filename
 
# playlistbox - contains just the filename
# Fullpath + filename is required to play the music inside start_music load function
 
 
#function to get the song from computer - It takes the path
def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_a_song(filename_path)
    mixer.music.queue(filename_path)
 
#function to add song into the list 
def add_a_song(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1
 
menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)
 
#function to display information about uus
def about_us():
    tkinter.messagebox.showinfo('About TuneMate', 'This is a music player build using Python Tkinter and Pygame')
 
 
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)
 
mixer.init()  # initializing the mixer
 
root.title("TuneMate")
root.iconbitmap(r'images/melody.ico')
 
 
#creating the left frame
leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=10, pady=10)
 
playlistbox = Listbox(leftframe)
playlistbox.pack()
 
addBtn = ttk.Button(leftframe, text="+ Add Song", command=browse_file)
addBtn.pack(side=LEFT, padx=10, pady=10)
 
 
#deleting the song from your listbox (playlist)
def delete_a_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)
 
 
delBtn = ttk.Button(leftframe, text="- Delete Song", command=delete_a_song)
delBtn.pack(side=LEFT)
 
rightframe = Frame(root)
rightframe.pack(pady=10)
 
topframe = Frame(rightframe)
topframe.pack()
 
lengthlabel = ttk.Label(topframe, text='Total Length : --:--')
lengthlabel.pack(pady=10)
 
currenttimelabel = ttk.Label(topframe, text='Current Time : --:--', relief=GROOVE)
currenttimelabel.pack()
 
#function to start the music
def start_music():
    global paused
 
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            view_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'TuneMate could not find the file. Please check again.')
 
            
#function to view details of currently playing song
def view_details(play_song):
    file_data = os.path.splitext(play_song)
 
    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()
 
    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat
 
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()
 
 
def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button 
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1
 
 
#function to stop the music
def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"
 
 
paused = FALSE
 
#function to rewind the music
def rewind_music():
    start_music()
    statusbar['text'] = "Music Rewinded"
 
 
#function to pause the music
def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"
 
 
#function to set the volume - value of volume ranges from 0 to 1
def set_volume(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
 
 
muted = FALSE
 
#function to mute volume
def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE
 
 
middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)
 
#Here we are adding images to buttons to make them look good
 
#Top frame of right side containing play, pause and stop controls
 
playPhoto = PhotoImage(file='images/play.png') 
playBtn = ttk.Button(middleframe, image=playPhoto, command=start_music)
playBtn.grid(row=0, column=0, padx=10)
 
stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)
 
pausePhoto = PhotoImage(file='images/pause.png')
pauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)
 
# Bottom Frame for volume, rewind, mute controls
 
bottomframe = Frame(rightframe)
bottomframe.pack()
 
rewindPhoto = PhotoImage(file='images/rewind.png')
rewindBtn = ttk.Button(bottomframe, image=rewindPhoto, command=rewind_music)
rewindBtn.grid(row=0, column=0)
 
mutePhoto = PhotoImage(file='images/mute.png')
volumePhoto = PhotoImage(file='images/volume.png')
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=1)
 
scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_volume)
scale.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)
 
 
#function called when we close the window.It stops the music and closes the window.
def on_closing():
    stop_music()
    root.destroy()
 
 
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop() #Making the application run
