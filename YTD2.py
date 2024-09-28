from pytube import YouTube
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from urllib.error import HTTPError
from pydub import AudioSegment

def download_video(url, save_path, file_name, download_type):
    try:
        yt = YouTube(url)

        if download_type == 'video':
            # Download video (highest resolution MP4)
            streams = yt.streams.filter(progressive=True, file_extension="mp4")
            highest_res_stream = streams.get_highest_resolution()
            highest_res_stream.download(output_path=save_path, filename=file_name + '.mp4')
            print("Video download was successful!")
            messagebox.showinfo("Success", "Video download was successful!")
        elif download_type == 'audio':
            # Download audio (MP3 format)
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_file = audio_stream.download(output_path=save_path, filename=file_name + '.mp4')
            mp3_path = convert_to_mp3(audio_file, save_path, file_name)
            if mp3_path:
                print("Audio download and conversion to MP3 was successful!")
                messagebox.showinfo("Success", "Audio download and conversion to MP3 was successful!")

    except HTTPError as e:
        if e.code == 410:
            print("Error: The video is no longer available (HTTP Error 410: Gone).")
            messagebox.showerror("Error", "The video is no longer available (HTTP Error 410: Gone).")
        else:
            print(f"HTTP Error {e.code}: {e.reason}")
            messagebox.showerror("Error", f"HTTP Error {e.code}: {e.reason}")
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", str(e))

def convert_to_mp3(video_file, save_path, file_name):
    try:
        # Set output MP3 filename
        mp3_path = os.path.join(save_path, file_name + '.mp3')
        
        # Convert video to audio (MP3)
        audio = AudioSegment.from_file(video_file)
        audio.export(mp3_path, format="mp3")
        
        # Delete the original video file
        os.remove(video_file)
        
        print(f"Conversion to MP3 completed: {mp3_path}")
        
        return mp3_path
    
    except Exception as e:
        print(f"Error converting to MP3: {e}")
        messagebox.showerror("Error", f"Error converting to MP3: {e}")
        return None

def open_file_dialog():
    folder = filedialog.askdirectory()
    if folder:
        print(f"Selected folder: {folder}")
    return folder

def start_download():
    video_url = url_entry.get()
    if not video_url:
        messagebox.showwarning("Input Error", "Please enter a YouTube URL")
        return

    file_name = file_name_entry.get()
    if not file_name:
        messagebox.showwarning("Input Error", "Please enter a file name")
        return

    save_dir = open_file_dialog()
    if not save_dir:
        messagebox.showwarning("Input Error", "Invalid save location")
        return

    download_type = messagebox.askyesno("Download Option", "Do you want to download the video (Yes) or just the audio (No)?")
    if download_type:
        print("Started video download, please wait")
        status_label.config(text="Downloading video, please wait...")
        root.update_idletasks()
        download_video(video_url, save_dir, file_name, 'video')
    else:
        print("Started audio download and conversion, please wait")
        status_label.config(text="Downloading audio, please wait...")
        root.update_idletasks()
        download_video(video_url, save_dir, file_name, 'audio')
    status_label.config(text="")

# Set up the Tkinter GUI
root = tk.Tk()
root.title("YouTube Downloader")

# URL input
tk.Label(root, text="YouTube URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# File name input
tk.Label(root, text="File Name:").grid(row=1, column=0, padx=10, pady=10)
file_name_entry = tk.Entry(root, width=50)
file_name_entry.grid(row=1, column=1, padx=10, pady=10)

# Download button
download_button = tk.Button(root, text="Download", command=start_download)
download_button.grid(row=2, column=0, columnspan=2, pady=20)

# Status label
status_label = tk.Label(root, text="")
status_label.grid(row=3, column=0, columnspan=2)

# Start the Tkinter event loop
root.mainloop()
