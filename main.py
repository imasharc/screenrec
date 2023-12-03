import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
import cv2
import numpy as np
import pyautogui
import threading
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageTk
import sounddevice as sd
from scipy.io.wavfile import write
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import time

class ScreenRecorderGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Screen Recorder")
        self.window.geometry("800x800")  # Set window size to 800x600

        # Initialize variables used in record
        self.recording = False
        self.start_time = None

        self.label = tk.Label(self.window, text="", font=("Arial", 14))
        self.label.pack(pady=10)

        # Canvas to display the captured screen
        self.canvas = Canvas(self.window, width=800, height=400, bg="white")
        self.canvas.pack()

        # Initialize variables used in create_image and create_oval
        self.img_tk = None
        self.mouse_x_main = 0
        self.mouse_y_main = 0

        # Label to display mouse cursor position
        self.mouse_label = tk.Label(self.window, text="Mouse Position: (0, 0)", font=("Arial", 12))
        self.mouse_label.pack(pady=5)

        # Audio recording
        self.audio_recording = None
        self.fs = 44100  # Sample rate
        self.recording_thread = None

        # Create a new ttk.Progressbar to display the audio level
        self.audio_level = ttk.Progressbar(self.window, length=200)
        self.audio_level.pack()

        tk.Button(self.window, text="Start Recording", command=self.start_recording, width=20).pack(pady=5)
        tk.Button(self.window, text="Stop Recording", command=self.stop_recording, width=20).pack()
    
    def start_audio_recording(self):
        self.audio_recording = sd.InputStream(samplerate=self.fs, channels=2, callback=self.audio_callback)
        self.audio_recording.start()
        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.start()
        self.visualizer_thread = threading.Thread(target=self.run_visualizer)
        self.visualizer_thread.start()

    def audio_callback(self, indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 10
        print("|" * int(volume_norm))  # For testing purposes
        self.audio_level['value'] = volume_norm

    def record_audio(self):
        audio_data = []
        self.output_audio_file = Path.home() / "Documents" / f"audio_{datetime.now().strftime('%Y%m%d%H%M%S')}.wav"
        print(f"Recording Audio file: {str(self.output_audio_file)}")
        while self.audio_recording.active:
            data, overflowed = self.audio_recording.read(1024)
            if not overflowed:
                audio_data.append(data)
        write(self.output_audio_file, self.fs, np.concatenate(audio_data))  # Save as WAV file

    def stop_audio_recording(self):
        if self.audio_recording is not None:
            self.audio_recording.stop()
            self.audio_recording.close()
            self.audio_recording = None
            self.recording_thread.join()  # Wait for the audio recording to finish
            if hasattr(self, 'visualizer_thread'):
                self.visualizer_thread.join()  # Wait for the visualizer to finish
            print(f"Finished recording audio file: {str(self.output_audio_file)}")
            if not self.output_audio_file.exists():
                print(f"Error: The file {str(self.output_audio_file)} does not exist.")

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.start_time = datetime.now()
            threading.Thread(target=self.record).start()
            self.start_audio_recording()  # Start audio recording

    def record(self):
        self.output_file = Path.home() / "Documents" / f"rec_{self.start_time.strftime('%Y%m%d%H%M%S')}.avi"
        print(f"Recording Video file: {str(self.output_file)}")
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(str(self.output_file), fourcc, 10, (800, 400))

        try:
            while self.recording:
                screenshot = pyautogui.screenshot()
                frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                frame_resized = cv2.resize(frame, (800, 400))
                frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                self.img_tk = ImageTk.PhotoImage(Image.fromarray(frame_rgb))

                mouse_x, mouse_y = pyautogui.position()
                self.mouse_label.config(text=f"Mouse Position: ({mouse_x}, {mouse_y})")

                self.canvas.delete("all")
                elapsed_time = datetime.now() - self.start_time
                self.label.config(text=str(elapsed_time))

                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)

                canvas_x = (mouse_x / screen_size.width) * 800
                canvas_y = (mouse_y / screen_size.height) * 400

                self.canvas.create_oval(canvas_x - 5, canvas_y - 5, canvas_x + 5, canvas_y + 5, fill="red")
                self.canvas.update()

                out.write(frame_resized)
        finally:
            out.release()

    def stop_recording(self):
        self.recording = False
        self.label.config(text="")
        self.mouse_label.config(text="Mouse Position: (0, 0)")
        self.stop_audio_recording()  # Stop audio recording

        # Create a new top-level window
        progress_window = tk.Toplevel(self.window)
        progress_window.title("Please wait")

        # Create a label and a progress bar
        label = tk.Label(progress_window, text="Saving file. This may take up to 3 seconds.")
        label.pack()
        progress = ttk.Progressbar(progress_window, length=200, mode='indeterminate')
        progress.pack()

        # Start the progress bar
        progress.start()

        # Wait for the video file to finish writing
        self.window.after(3000, self.merge_audio_video)  # Merge audio and video after 15 seconds

        # Close the progress window after 15 seconds
        self.window.after(3000, progress_window.destroy)

    def merge_audio_video(self):
        print(f"Video file: {str(self.output_file)}")
        video = VideoFileClip(str(self.output_file))
        print(f"Audio file: {str(self.output_audio_file)}")
        audio = AudioFileClip(str(self.output_audio_file))
        video = video.set_audio(audio)
        final_output_file = Path.home() / "Documents" / f"rec_{self.start_time.strftime('%Y%m%d%H%M%S')}.mp4"
        video.write_videofile(str(final_output_file), codec='libx264')

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRecorderGUI(root)
    root.mainloop()