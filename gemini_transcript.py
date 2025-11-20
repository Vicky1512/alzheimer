import google.generativeai as genai
import os
import shutil

genai.configure()
model = genai.GenerativeModel("gemini-2.0-flash")


def transcribe_audio(file_path):
    with open(file_path, "rb") as f:
        audio_bytes = f.read()

    response = model.generate_content([
        "Transcribe the following audio:",
        {"mime_type": "audio/wav", "data": audio_bytes},
    ])

    return response.text


def process_and_archive(wav_path):
    print(f"Transcribing: {wav_path}")
    transcript = transcribe_audio(wav_path)

    # output transcript path
    os.makedirs("Transcripts", exist_ok=True)
    base = os.path.basename(wav_path)
    transcript_path = f"Transcripts/{base}_transcript.txt"

    # save transcript
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    print(f"Saved transcript → {transcript_path}")

    # archive audio
    archive_dir = "Recordings/Processed"
    os.makedirs(archive_dir, exist_ok=True)

    shutil.move(wav_path, f"{archive_dir}/{os.path.basename(wav_path)}")
    print(f"Archived WAV → {archive_dir}")

    return transcript_path  # <--- needed by Program 1
