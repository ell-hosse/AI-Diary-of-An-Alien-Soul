from PIL import Image
import os
import sys
from datetime import datetime
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
METADATA_PATH = ROOT / "metadata.json"
ORIGINAL_DIR = ROOT / "images" / "original"
THUMBS_DIR = ROOT / "images" / "thumbs"
README_PATH = ROOT / "README.md"

COMPRESSED_WIDTH = 1200
THUMB_WIDTH = 300

os.makedirs(THUMBS_DIR, exist_ok=True)

def update_image_preview_version() -> None:
    try:
        text = README_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        print("README.md not found – skipping preview bump.")
        return

    pattern = re.compile(r"\?v=(\d{7})")
    match = pattern.search(text)

    if match:
        old_num = int(match.group(1))
        new_num = 1 if old_num >= 9_999_999 else old_num + 1
        replacement = f"?v={new_num:07d}"
        bumped = pattern.sub(replacement, text, count=1)
        print(f"✔ Preview version bumped: {old_num:07d} → {new_num:07d}")
    else:
        bumped = text.replace(
            'AI-Diary-of-An-Alien-Soul/"',
            'AI-Diary-of-An-Alien-Soul/?v=0000001"',
            1
        )
        print("✔ Preview version added: 0000001")

    README_PATH.write_text(bumped, encoding="utf-8")

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

    update_image_preview_version()
