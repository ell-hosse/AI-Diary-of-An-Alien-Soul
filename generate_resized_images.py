from PIL import Image
import os
import sys

ORIGINAL_DIR = 'images/original'
THUMBS_DIR = 'images/thumbs'

# Sizes
COMPRESSED_WIDTH = 1200
THUMB_WIDTH = 300

os.makedirs(THUMBS_DIR, exist_ok=True)

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
For running over one single file: python generate_resized_images.py "ChatGPT Image Apr 16, 2025, 12_54_00 PM.png"
'''
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage:")
        print("   python generate_resized_images.py all")
        print("   python generate_resized_images.py <filename>")
    elif sys.argv[1] == "all":
        convert_all_images()
    else:
        convert_single_image(sys.argv[1])
