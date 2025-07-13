from PIL import Image
import os
import sys
from datetime import datetime
import json

METADATA_PATH = "metadata.json"
ORIGINAL_DIR = 'images/original'
THUMBS_DIR = 'images/thumbs'

COMPRESSED_WIDTH = 1200
THUMB_WIDTH = 300

os.makedirs(THUMBS_DIR, exist_ok=True)

def extract_creation_date(filename: str) -> str:
    base = os.path.splitext(filename)[0]
    prefix = "ChatGPT Image "
    if base.startswith(prefix):
        date_str = base[len(prefix):]
    else:
        date_str = base
    dt = datetime.strptime(date_str, "%b %d, %Y, %I_%M_%S %p")
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def add_metadata_entry(filename: str, title: str):
    try:
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    new_entry = {
        "filename": filename,
        "title": title,
        "creation_date": extract_creation_date(filename)
    }

    data.append(new_entry)

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✔ Added metadata entry for {filename!r}")

def resize_and_save(image_path, filename):
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")

        # Thumbnail version
        ratio_t = THUMB_WIDTH / img.width
        thumb_img = img.resize(
            (THUMB_WIDTH, int(img.height * ratio_t)), Image.LANCZOS)
        thumb_img.save(os.path.join(THUMBS_DIR, filename), optimize=True, quality=80)

        print(f"✔ Done: {filename}")

    except Exception as e:
        print(f"Error processing {filename}: {e}")

def convert_all_images():
    for filename in os.listdir(ORIGINAL_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            original_path = os.path.join(ORIGINAL_DIR, filename)
            resize_and_save(original_path, filename)

def convert_single_image(filename):
    path = os.path.join(ORIGINAL_DIR, filename)
    if not os.path.exists(path):
        print(f"File not found: {filename}")
        return
    resize_and_save(path, filename)

'''
For running over all images: python generate_resized_images.py all
For running over one single file: python generate_resized_images.py "ChatGPT Image Apr 16, 2025, 12_54_00 PM.png" "title"
'''
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage:")
        print("python generate_resized_images.py all")
        print("python generate_resized_images.py <filename> <[!optional] title>")
        sys.exit(1)

    if sys.argv[1].lower() == "all":
        convert_all_images()
    else:
        filename = sys.argv[1]
        title = sys.argv[2] if len(sys.argv) >= 3 else None

        convert_single_image(filename)

        if title:
            add_metadata_entry(filename, title)
