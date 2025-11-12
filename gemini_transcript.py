from google import genai
import os
import glob

# Optionally set your key explicitly
# client = genai.Client(api_key="YOUR_GEMINI_API_KEY")
client = genai.Client()  # will use env var GEMINI_API_KEY
def processed_text(filename):
    print(f"Transcribing: {filename}")
    transcript = transcribe_audio(filename, model="gemini-2.0-flash")
    print("Transcript:")
    print(transcript)

    # Optionally save to .txt file
    out_dir = "Transcripts"
    os.makedirs(out_dir, exist_ok=True)
     
    base_name = os.path.basename(filename)
    transcript_name = os.path.join(out_dir, base_name+"_transcript.txt")
    with open(transcript_name, "w", encoding="utf-8") as f:
        f.write(transcript)
    print(f"Saved transcript to {transcript_name}")

def move_to_archive(filename):
    archive_dir = "Recordings/Processed"
    os.makedirs(archive_dir, exist_ok=True)
    
    base_name = os.path.basename(filename)
    new_path = os.path.join(archive_dir, base_name)
    os.rename(filename, new_path)
    print(f"Moved {filename} to {new_path}")

def transcribe_audio(file_path: str, model: str = "gemini-2.0-flash"):
    # Read audio file as bytes
    with open(file_path, "rb") as f:
        audio_bytes = f.read()

    # Create request: Provide prompt + file part
    prompt = "Transcribe the following audio file."
    # Import types for constructing parts
    from google.genai import types

    response = client.models.generate_content(
        model=model,
        contents=[
            prompt,
            types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav")
        ]
    )
    return response.text

def process_and_archive(filename):
    processed_text(filename)
    move_to_archive(filename)

if __name__ == "__main__":
    files = glob.glob("Recordings/Unprocessed/*.wav")
    os.makedirs("Transcripts", exist_ok=True)
    for path in files:
        process_and_archive(path)