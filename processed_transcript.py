import os
import google.generativeai as genai

# -------------------- CONFIG --------------------
# Set your Gemini API key
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Model name
MODEL_NAME = "gemini-1.5-pro"  # or whichever version you want

# Folders
input_folder = "path/to/transcriptions"         # folder with .txt files
output_folder = "path/to/gemini_responses"      # folder to save responses

# Make sure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Custom prompt to send to Gemini
# You can make this dynamic if needed
prompt_prefix = "Summarize this transcription clearly and concisely:\n\n"

# -------------------- PROCESS FILES --------------------
model = genai.GenerativeModel(MODEL_NAME)

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
