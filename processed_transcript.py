import os
import shutil
import google.generativeai as genai

genai.configure()
model = genai.GenerativeModel("gemini-2.0-flash")

INPUT_FOLDER = "Transcripts"
OUTPUT_FOLDER = "Transcriptions_Summaries"
ARCHIVE_FOLDER = "Processed_Transcripts_Archive"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

prompt_prefix = (
    "What song is grandpa trying to remember in this conversation? "
    "Give a list of 10 likely songs with YouTube links:\n\n"
)


def process_file(path):
    filename = os.path.basename(path)
    output_path = f"{OUTPUT_FOLDER}/{filename}"

    # skip duplicates
    if os.path.exists(output_path):
        print(f"Skipping {filename}, already processed.")
        return

    # read transcript
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Ask Gemini
    response = model.generate_content(prompt_prefix + text)
    summary = response.text.strip()

    # save processed output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"Processed → {output_path}")


def process_and_archive(path):
    process_file(path)

    # archive transcript
    filename = os.path.basename(path)
    shutil.move(path, f"{ARCHIVE_FOLDER}/{filename}")
    print(f"Archived transcript → {ARCHIVE_FOLDER}/{filename}")
