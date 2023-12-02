import subprocess
import sys

def install_libraries():
    try:
        # Install required Python libraries
        subprocess.run([sys.executable, "-m", "pip", "install", "opencv-python", "pyautogui", "Pillow", "screeninfo", "sounddevice", "scipy"])

        print("Libraries installed successfully!")

    except Exception as e:
        print(f"Error installing libraries: {e}")

if __name__ == "__main__":
    install_libraries()