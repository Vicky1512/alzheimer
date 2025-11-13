import os
import google.generativeai as genai

# -------------------- CONFIG --------------------
# Set your Gemini API key
genai.configure()

# Model name
MODEL_NAME = "gemini-2.0-flash"  # or whichever version you want

# Folders
input_folder = "Transcripts"         # folder with .txt files
output_folder = "Transcriptions_Summaries"      # folder to save responses
archive_folder = "Processed_Transcripts_Archive"
# Make sure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Custom prompt to send to Gemini
prompt_prefix = "What song is granmda trying to remember in this conversation. give me a list of 10 suggestions that are most likely the song with youtube links:\n\n"

# -------------------- PROCESS FILES --------------------
model = genai.GenerativeModel(MODEL_NAME)

#def move_to_archive(filename):
#    archive_dir = archive_folder
#    os.makedirs(archive_dir, exist_ok=True)
#
#    base_name = os.path.basename(filename)
#    new_path = os.path.join(archive_dir, base_name)
#    os.rename(filename, new_path)
#    print(f"Moved {filename} to {new_path}")

def main_process():
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

        # Skip if response already exists
        if os.path.exists(output_path):
            print(f"Skipping {filename}, already processed.")
            continue

        # Read input text
        with open(input_path, "r", encoding="utf-8") as f:
            text_content = f.read()

        # Combine prompt + text
        prompt = prompt_prefix + text_content

        # Send to Gemini
        try:
            response = model.generate_content(prompt)
            result_text = response.text.strip()
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue

        # Write Gemini’s output to a new .txt file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result_text)

        print(f"✅ Processed {filename} → saved response to {output_path}")
        


print("All files processed!")
