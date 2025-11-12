import tkinter as tk
import sounddevice as sd
import wavio
import threading
import datetime
import os

import gemini_transcript  # Import the transcription module

# Settings
SAMPLE_RATE = 44100  # 44.1 kHz
CHANNELS = 2         # Stereo

recording = False
audio_data = []

def record_audio():
    global recording, audio_data
    audio_data = []
    recording = True

    def callback(indata, frames, time, status):
        if recording:
            audio_data.append(indata.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback):
        while recording:
            sd.sleep(100)

def start_recording():
    status_label.config(text="🎙️ Recording...")
    record_button.config(state="disabled")
    stop_button.config(state="normal")
    threading.Thread(target=record_audio).start()

def stop_recording():
    global recording
    recording = False
    status_label.config(text="✅ Recording stopped.")
    record_button.config(state="normal")
    stop_button.config(state="disabled")

    if audio_data:
        # Combine all recorded chunks
        import numpy as np
        audio = np.concatenate(audio_data, axis=0)

        # Save with timestamp
        if not os.path.exists("Recordings/Unprocessed"):
            os.makedirs("Recordings/Unprocessed")
        filename = f"Recordings/Unprocessed/recording_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        wavio.write(filename, audio, SAMPLE_RATE, sampwidth=2)
        status_label.config(text=f"💾 Saved as {filename}")

        gemini_transcript.process_and_archive(filename)  # Transcribe and archive the recording

# --- GUI Setup ---
root = tk.Tk()
root.title("Simple Voice Recorder")
root.geometry("300x180")

record_button = tk.Button(root, text="🎤 Start Recording", command=start_recording, bg="red", fg="white", font=("Arial", 12))
record_button.pack(pady=20)

stop_button = tk.Button(root, text="⏹ Stop Recording", command=stop_recording, bg="gray", fg="white", font=("Arial", 12), state="disabled")
stop_button.pack(pady=10)

status_label = tk.Label(root, text="Press 'Start Recording' to begin.", font=("Arial", 10))
status_label.pack(pady=10)

root.mainloop()
