import os
import pygame
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pygame import mixer
from tkinter import ttk
from PIL import Image, ImageTk

# Initialize Pygame mixer
pygame.mixer.init()

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Music Player")
        self.root.geometry("600x500")
        self.root.config(bg="#1a1a1a")

        self.current_song = None
        self.is_playing = False
        self.is_paused = False

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        self.title_label = tk.Label(self.root, text="Python Music Player", font=("Helvetica", 20, 'bold'), bg="#1a1a1a", fg="white")
        self.title_label.grid(row=0, column=0, columnspan=4, pady=20)

        # Song Listbox Frame
        self.song_frame = ttk.Frame(self.root)
        self.song_frame.grid(row=1, column=0, columnspan=4, pady=10, padx=20, sticky="ew")

        # Song Listbox
        self.song_listbox = tk.Listbox(self.song_frame, width=50, height=10, bg="#333333", fg="white", selectmode=tk.SINGLE, font=("Arial", 12))
        self.song_listbox.pack(side="left", fill="both", expand=True)
        
        # Scrollbar for Listbox
        self.scrollbar = ttk.Scrollbar(self.song_frame, orient="vertical", command=self.song_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.song_listbox.config(yscrollcommand=self.scrollbar.set)

        # Control Buttons Frame
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.grid(row=2, column=0, columnspan=4, pady=20)

        # Add Play Button with Image
        self.play_image = self.load_image("play_icon.png", (50, 50))
        self.play_button = ttk.Button(self.control_frame, image=self.play_image, command=self.play_song, style="TButton")
        self.play_button.grid(row=0, column=0, padx=15)

        # Add Pause Button with Image
        self.pause_image = self.load_image("pause_icon.png", (50, 50))
        self.pause_button = ttk.Button(self.control_frame, image=self.pause_image, command=self.pause_song, style="TButton")
        self.pause_button.grid(row=0, column=1, padx=15)

        # Add Stop Button with Image
        self.stop_image = self.load_image("stop_icon.png", (50, 50))
        self.stop_button = ttk.Button(self.control_frame, image=self.stop_image, command=self.stop_song, style="TButton")
        self.stop_button.grid(row=0, column=2, padx=15)

        # Add Next Button with Image
        self.next_image = self.load_image("next_icon.png", (50, 50))
        self.next_button = ttk.Button(self.control_frame, image=self.next_image, command=self.next_song, style="TButton")
        self.next_button.grid(row=0, column=3, padx=15)

        # Add Previous Button with Image
        self.prev_image = self.load_image("prev_icon.png", (50, 50))
        self.prev_button = ttk.Button(self.control_frame, image=self.prev_image, command=self.prev_song, style="TButton")
        self.prev_button.grid(row=0, column=4, padx=15)

        # Volume Control Frame
        self.volume_frame = ttk.Frame(self.root)
        self.volume_frame.grid(row=3, column=0, columnspan=4, pady=10, padx=20, sticky="ew")

        self.volume_label = tk.Label(self.volume_frame, text="Volume", bg="#1a1a1a", fg="white", font=("Arial", 12))
        self.volume_label.grid(row=0, column=0, padx=10)

        self.volume_scale = ttk.Scale(self.volume_frame, from_=0, to=1, orient="horizontal", command=self.set_volume)
        self.volume_scale.set(0.5)  # Default volume 50%
        self.volume_scale.grid(row=0, column=1, padx=10, sticky="ew")

        # Browse Button
        self.browse_button = ttk.Button(self.root, text="Browse Music Files", command=self.browse_files, style="TButton")
        self.browse_button.grid(row=4, column=0, columnspan=4, pady=20)

        # Now Playing Label
        self.now_playing_label = tk.Label(self.root, text="Now Playing: None", font=("Arial", 12), bg="#1a1a1a", fg="white")
        self.now_playing_label.grid(row=5, column=0, columnspan=4, pady=10)

    def load_image(self, img_name, size=(40, 40)):
        """Load an image and resize it."""
        try:
            img = Image.open(img_name)
            img = img.resize(size, Image.ANTIALIAS)
            return ImageTk.PhotoImage(img)
        except:
            messagebox.showerror("Error", f"Error loading image: {img_name}")
            return None

    def browse_files(self):
        """Browse for music files and load them into the listbox."""
        file_types = [("MP3 Files", "*.mp3"), ("All Files", "*.*")]
        files = filedialog.askopenfilenames(title="Choose Music Files", filetypes=file_types)
        if files:
            self.song_listbox.delete(0, tk.END)
            for file in files:
                self.song_listbox.insert(tk.END, os.path.basename(file))

    def play_song(self):
        """Play selected song."""
        if self.song_listbox.curselection():
            song_index = self.song_listbox.curselection()[0]
            song_name = self.song_listbox.get(song_index)
            song_path = filedialog.askopenfilename(title="Choose Music File")
            
            if self.is_paused:
                mixer.music.unpause()
                self.is_playing = True
                self.is_paused = False
            else:
                song_path = os.path.join(self.song_listbox.get(song_index))
                mixer.music.load(song_path)
                mixer.music.play()
                self.is_playing = True
                self.is_paused = False

            self.current_song = song_name
            self.now_playing_label.config(text=f"Now Playing: {self.current_song}")

    def pause_song(self):
        """Pause the current song."""
        if self.is_playing and not self.is_paused:
            mixer.music.pause()
            self.is_paused = True

    def stop_song(self):
        """Stop the current song."""
        if self.is_playing:
            mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            self.now_playing_label.config(text="Now Playing: None")

    def next_song(self):
        """Play the next song in the list."""
        if self.song_listbox.curselection():
            song_index = self.song_listbox.curselection()[0] + 1
            if song_index >= self.song_listbox.size():
                song_index = 0
            self.song_listbox.select_set(song_index)
            self.play_song()

    def prev_song(self):
        """Play the previous song in the list."""
        if self.song_listbox.curselection():
            song_index = self.song_listbox.curselection()[0] - 1
            if song_index < 0:
                song_index = self.song_listbox.size() - 1
            self.song_listbox.select_set(song_index)
            self.play_song()

    def set_volume(self, volume):
        """Set the volume for the music."""
        mixer.music.set_volume(float(volume))

# Create Tkinter window and run the music player
root = tk.Tk()
player = MusicPlayer(root)
root.mainloop()
