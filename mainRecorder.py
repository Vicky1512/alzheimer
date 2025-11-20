import tkinter as tk
import sounddevice as sd
import wavio
import threading
import datetime
import os
import numpy as np

import gemini_transcript
import processed_transcript

SAMPLE_RATE = 44100
CHANNELS = 2

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
    status_label.config(text="⏹ Recording stopped.")
    record_button.config(state="normal")
    stop_button.config(state="disabled")

    if audio_data:
        audio = np.concatenate(audio_data, axis=0)

        # Ensure folder exists
        os.makedirs("Recordings/Unprocessed", exist_ok=True)

        # Save WAV
        filename = f"Recordings/Unprocessed/recording_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        wavio.write(filename, audio, SAMPLE_RATE, sampwidth=2)
        status_label.config(text=f"Saved: {filename}")

        # 1️⃣ Transcribe WAV → saves transcript + archives WAV
        transcript_path = gemini_transcript.process_and_archive(filename)

        # 2️⃣ Process transcript → outputs summary
        processed_transcript.process_and_archive(transcript_path)


# GUI ----------------
root = tk.Tk()
root.title("Voice Recorder")
root.geometry("300x180")

record_button = tk.Button(root, text="🎤 Start Recording", command=start_recording, bg="red", fg="white")
record_button.pack(pady=20)

stop_button = tk.Button(root, text="⏹ Stop Recording", command=stop_recording,
                        bg="gray", fg="white", state="disabled")
stop_button.pack(pady=10)

status_label = tk.Label(root, text="Press Start Recording")
status_label.pack(pady=10)

root.mainloop()
