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
prompt_prefix = "transcirbe this message into questions and \n\n"

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

    all_conversations = []
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

        # Skip if response already exists
       # if os.path.exists(output_path):
         #   print(f"Skipping {filename}, already processed.")
         #   continue
    
        # Read input text
        with open(input_path, "r", encoding="utf-8") as f:
            text_content = f.read()
            all_conversations.append(text_content)


    # Combine prompt + text
    prompt = prompt_prefix +"\n\n" + "\n\n".join(all_conversations)
    prompt += "\n\nPlease provide a concise summary of the above conversations."

    while True:
        # Send to Gemini
        try:
            response = model.generate_content(prompt)
            result_text = response.text.strip()
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue

        print(f"Gemini response:\n{result_text}\n")

        user_input = input("Tell me what you want to do next...")
        if user_input.lower() == "exit":
            print("Exiting the processing loop.")
            break

        prompt += f"\n\nUser Input: {user_input}\nPlease adjust the response accordingly."

        # Write Gemini’s output to a new .txt file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result_text)

        print(f"✅ Processed {filename} → saved response to {output_path}")
        
main_process()

print("All files processed!")
