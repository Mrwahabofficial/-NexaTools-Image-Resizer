import os
import sys

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def clean_path(path):
    return path.strip().strip('"').strip("'").strip()

def print_header():
    print("=" * 60)
    print("  Image Resizer Pro — NexaTools")
    print("  Resize, convert and optimize images instantly")
    print("=" * 60)

def get_resize_options():
    print("\nResize Options:")
    print("  1. Resize to custom width and height")
    print("  2. Resize by percentage")
    print("  3. Resize to preset sizes")
    print()
    choice = input("Enter choice (1/2/3): ").strip()
    
    if choice == "1":
        width = int(input("Enter width (pixels): ").strip())
        height = int(input("Enter height (pixels): "))
        return ("custom", width, height)
    
    elif choice == "2":
        percent = float(input("Enter percentage (e.g. 50 for 50%): ").strip())
        return ("percent", percent)
    
    elif choice == "3":
        print("\nPreset Sizes:")
        print("  1. HD        — 1280 x 720")
        print("  2. Full HD   — 1920 x 1080")
        print("  3. 4K        — 3840 x 2160")
        print("  4. Thumbnail — 150 x 150")
        print("  5. Square    — 500 x 500")
        print("  6. Profile   — 400 x 400")
        preset = input("\nChoose preset (1-6): ").strip()
        presets = {
            "1": (1280, 720),
            "2": (1920, 1080),
            "3": (3840, 2160),
            "4": (150, 150),
            "5": (500, 500),
            "6": (400, 400)
        }
        size = presets.get(preset, (1280, 720))
        return ("custom", size[0], size[1])
    
    return ("custom", 800, 600)

def get_output_format():
    print("\nOutput Format:")
    print("  1. Keep original format")
    print("  2. JPG")
    print("  3. PNG")
    print("  4. WEBP")
    choice = input("Choose format (1/2/3/4): ").strip()
    formats = {"1": None, "2": "JPEG", "3": "PNG", "4": "WEBP"}
    return formats.get(choice, None)

def resize_image(img_path, output_dir, resize_option, output_format, quality):
    from PIL import Image
    
    img = Image.open(img_path)
    original_size = img.size
    filename = os.path.basename(img_path)
    name, ext = os.path.splitext(filename)
    
    if resize_option[0] == "custom":
        new_size = (resize_option[1], resize_option[2])
        img = img.resize(new_size, Image.LANCZOS)
    
    elif resize_option[0] == "percent":
        percent = resize_option[1] / 100
        new_width = int(img.width * percent)
        new_height = int(img.height * percent)
        img = img.resize((new_width, new_height), Image.LANCZOS)
    
    if output_format:
        ext = ".jpg" if output_format == "JPEG" else f".{output_format.lower()}"
    
    output_filename = f"{name}_resized{ext}"
    output_path = os.path.join(output_dir, output_filename)
    
    if output_format == "JPEG" or ext.lower() in ['.jpg', '.jpeg']:
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        img.save(output_path, "JPEG", quality=quality)
    else:
        img.save(output_path, quality=quality)
    
    return original_size, img.size, output_path

def main():
    clear()
    print_header()
    
    try:
        from PIL import Image
    except ImportError:
        print("\n[SETUP] Installing required library...")
        os.system(f"{sys.executable} -m pip install Pillow -q")
        print("[DONE] Library installed!\n")
    
    print("\nHow do you want to add images?")
    print("  1. Single image")
    print("  2. Multiple images")
    print("  3. Entire folder")
    print()
    source = input("Enter choice (1/2/3): ").strip()
    
    images = []
    
    if source == "1":
        raw = input("\nImage path (Right click → Copy as path): ")
        path = clean_path(raw)
        if os.path.exists(path):
            images.append(path)
        else:
            print(f"  [ERROR] File not found: {path}")
            return
    
    elif source == "2":
        print("\nEnter image paths one by one.")
        print("Press Enter twice when done.\n")
        while True:
            raw = input(f"Image {len(images)+1}: ")
            path = clean_path(raw)
            if not path:
                if len(images) >= 1:
                    break
                continue
            if os.path.exists(path):
                images.append(path)
                print(f"  [ADDED] {os.path.basename(path)} ✓")
            else:
                print(f"  [ERROR] File not found!")
    
    elif source == "3":
        raw = input("\nFolder path: ")
        folder = clean_path(raw)
        if not os.path.exists(folder):
            print("[ERROR] Folder not found!")
            return
        extensions = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif']
        images = [
            os.path.join(folder, f) 
            for f in os.listdir(folder) 
            if os.path.splitext(f)[1].lower() in extensions
        ]
        print(f"\nFound {len(images)} images!")
    
    if not images:
        print("[ERROR] No images found!")
        return
    
    resize_option = get_resize_options()
    output_format = get_output_format()
    
    quality = input("\nImage quality 1-100 [85]: ").strip()
    quality = int(quality) if quality else 85
    
    raw_out = input("\nOutput folder [resized_images]: ").strip()
    output_dir = clean_path(raw_out) if raw_out else "resized_images"
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "-" * 60)
    print(f"Images to resize  : {len(images)}")
    print(f"Output folder     : {output_dir}")
    print(f"Quality           : {quality}%")
    print("-" * 60)
    
    confirm = input("\nProceed? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Cancelled.")
        return
    
    print("\nResizing...")
    success = 0
    for img_path in images:
        try:
            original, new, out = resize_image(
                img_path, output_dir, 
                resize_option, output_format, quality
            )
            print(f"  [DONE] {os.path.basename(img_path)}")
            print(f"         {original[0]}x{original[1]} → {new[0]}x{new[1]}")
            success += 1
        except Exception as e:
            print(f"  [ERROR] {os.path.basename(img_path)}: {e}")
    
    print("\n" + "=" * 60)
    print("  Resize Complete!")
    print(f"  Images resized  : {success}/{len(images)}")
    print(f"  Saved to        : {output_dir}")
    print("=" * 60)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
