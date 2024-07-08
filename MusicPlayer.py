import os
import fnmatch
import customtkinter as ctk
from tkinter import Listbox, Scrollbar
from PIL import Image, ImageTk
from pygame import mixer, USEREVENT
import pygame

# Initializing pygame to create events
pygame.init()

# Backend code
global is_manual_seek
is_manual_seek = False

def play_selected_song(event=None):
    global is_manual_seek
    seek.set(0)
    selected_song = listBox.get("anchor")
    if selected_song != ' ':
        current_label.configure(text=selected_song)
        mixer.music.load(os.path.join(path, selected_song))
        mixer.music.play()
        pauseButton.configure(image=pause_img)
        song_length = mixer.Sound(os.path.join(path, selected_song)).get_length()
        seek.configure(to=song_length)
        is_manual_seek = False

def pause_song():
    if mixer.music.get_busy():
        mixer.music.pause()
        pauseButton.configure(image=play_img)
    else:
        mixer.music.unpause()
        pauseButton.configure(image=pause_img)

def play_next():
    if listBox.curselection():
        next_song_index = (listBox.curselection()[0] + 2) % listBox.size()
        next_song_name = listBox.get(next_song_index)
        current_label.configure(text=next_song_name)
        mixer.music.load(os.path.join(path, next_song_name))
        mixer.music.play()
        listBox.select_clear(0, 'end')
        listBox.activate(next_song_index)
        listBox.select_set(next_song_index)
        song_length = mixer.Sound(os.path.join(path, next_song_name)).get_length()
        seek.configure(to=song_length)
        seek.set(0)

def play_prev():
    if listBox.curselection():
        prev_song_index = (listBox.curselection()[0] - 2) % listBox.size()
        prev_song_name = listBox.get(prev_song_index)
        current_label.configure(text=prev_song_name)
        mixer.music.load(os.path.join(path, prev_song_name))
        mixer.music.play()
        listBox.select_clear(0, 'end')
        listBox.activate(prev_song_index)
        listBox.select_set(prev_song_index)
        song_length = mixer.Sound(os.path.join(path, prev_song_name)).get_length()
        seek.configure(to=song_length)
        seek.set(0)

def check_music_end():
    for event in pygame.event.get():
        if mixer.music.get_busy():
            seek.set(seek.get()+1)
        if event.type == USEREVENT + 1:
            play_next()
    canvas.after(100, check_music_end)

# Front end

# Setting up a canvas
canvas = ctk.CTk()
canvas.title("Music Player")
canvas.geometry("700x600")
canvas.configure(fg_color="black")

head = {'fg_color': 'black', 'text_color': 'cyan', 'font': ('Open Sans', 36, 'bold')}

heading = ctk.CTkLabel(canvas, text='Your Library', **head)
heading.pack(pady=15, anchor='center')

# Frame to hold listbox and scrollbar
listbox_frame = ctk.CTkFrame(canvas, border_width=10, border_color='black')
listbox_frame.pack(padx=25, pady=15, fill='both', expand=True)

# Adding scrollbar
scrollbar = Scrollbar(listbox_frame, background='black', activebackground='black', troughcolor='black')
scrollbar.pack(side='right', fill='y')

# We are gonna put music here
listBox = Listbox(listbox_frame, fg="sky blue", bg="gray5", width=100, font=('ds-digital', 19), borderwidth=2, highlightthickness=2, relief='flat', yscrollcommand=scrollbar.set)
listBox.pack(side='left', fill='both', expand=True)
scrollbar.config(command=listBox.yview)

listBox.bind("<<ListboxSelect>>", play_selected_song)

# Fetching music from directory and displaying it on our canvas
path = r'D:\khushi\musicplayer\music'
pattern = r'*.mp3'
for root, dirs, file in os.walk(path):
    for filename in fnmatch.filter(file, pattern):
        listBox.insert('end', filename)
        listBox.insert('end', ' ')

# Displaying selected songs
current_label = ctk.CTkLabel(master=canvas, text=' ', fg_color='black', text_color='sky blue', font=('ds-digital', 20))
current_label.pack(pady=30)

# To display a seek

def update_playback_position(value): # To play the song when manually seeked
  selected_song = listBox.get("anchor")
  global is_manual_seek
  is_manual_seek = True
  mixer.music.play(start=int (value))
  is_manual_seek = False

seek = ctk.CTkSlider(master=canvas, from_=0, to=100, height=20, command=update_playback_position)
seek.pack(fill='x')

# To put buttons
top = ctk.CTkFrame(master=canvas, fg_color='black')
top.pack(padx=10, pady=20, anchor='center')

# Adding buttons with improved styling
button_style = {'fg_color': 'black', 'text_color': 'white', 'font': ('ds-digital', 15)}

# Load images using PIL and resize them
def resize_image(img_path, size):
    img = Image.open(img_path)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

prev_img = resize_image('prev_icon.png', (50, 50))
prevButton = ctk.CTkButton(master=top, image=prev_img, command=play_prev, text='', width=50, **button_style)
prevButton.pack(pady=15, side='left', padx=15)

pause_img = resize_image('pause_icon.png', (50, 50))
play_img = resize_image('play_icon.png', (50, 50))
pauseButton = ctk.CTkButton(master=top, image=play_img, command=pause_song, text='', width=50, **button_style)
pauseButton.pack(pady=15, side='left', padx=15)

next_img = resize_image('next_icon.png', (50, 50))
nextButton = ctk.CTkButton(master=top, image=next_img, command=play_next, text='', width=50, **button_style)
nextButton.pack(pady=15, side='left', padx=15)

# Initializing the mixer
mixer.init()
seek.set(0)

mixer.music.set_endevent(USEREVENT + 1)
check_music_end()

canvas.mainloop()
mixer.quit()
pygame.quit()