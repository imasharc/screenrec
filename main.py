import tkinter as tk
from tkinter import Canvas
import cv2
import numpy as np
import pyautogui
import threading
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageTk

class ScreenRecorderGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Screen Recorder")
        self.master.geometry("800x600")  # Set window size to 800x600

        self.recording = False
        self.start_time = None

        self.label = tk.Label(self.master, text="", font=("Arial", 14))
        self.label.pack(pady=10)

        # Canvas to display the captured screen
        self.canvas = Canvas(self.master, width=800, height=400, bg="white")
        self.canvas.pack()

        # Initialize variables used in create_image and create_oval
        self.img_tk = None
        self.mouse_x_main = 0
        self.mouse_y_main = 0

        # Label to display mouse cursor position
        self.mouse_label = tk.Label(self.master, text="Mouse Position: (0, 0)", font=("Arial", 12))
        self.mouse_label.pack(pady=5)

        tk.Button(self.master, text="Start Recording", command=self.start_recording, width=20).pack(pady=5)
        tk.Button(self.master, text="Stop Recording", command=self.stop_recording, width=20).pack()

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.start_time = datetime.now()
            threading.Thread(target=self.record).start()

    def record(self):
        screen_size = pyautogui.size()
        output_file = Path.home() / "Documents" / f"rec_{datetime.now().strftime('%Y%m%d%H%M%S')}.avi"
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(str(output_file), fourcc, 10, (800, 400))

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

        out.release()

    def stop_recording(self):
        self.recording = False
        self.label.config(text="")
        self.mouse_label.config(text="Mouse Position: (0, 0)")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRecorderGUI(root)
    root.mainloop()