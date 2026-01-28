"""Optimize images for web - creates WebP thumbnails"""
from pathlib import Path
from PIL import Image

PHOTOS_DIR = Path(__file__).parent / "photos"
THUMBS_DIR = PHOTOS_DIR / "thumbs"
THUMB_SIZE = (600, 400)  # Max dimensions for thumbnails
QUALITY = 80

THUMBS_DIR.mkdir(exist_ok=True)

for img_path in PHOTOS_DIR.glob("*"):
    if img_path.is_file() and img_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
        print(f"Processing {img_path.name}...")
        
        with Image.open(img_path) as img:
            # Convert to RGB if necessary
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Resize maintaining aspect ratio
            img.thumbnail(THUMB_SIZE, Image.Resampling.LANCZOS)
            
            # Save as WebP
            output_name = img_path.stem.lower().replace(" ", "-").replace(".", "-") + ".webp"
            output_path = THUMBS_DIR / output_name
            img.save(output_path, "WEBP", quality=QUALITY, optimize=True)
            
            # Get file sizes
            orig_size = img_path.stat().st_size / 1024
            new_size = output_path.stat().st_size / 1024
            print(f"  {orig_size:.1f}KB -> {new_size:.1f}KB ({100 - (new_size/orig_size*100):.0f}% smaller)")

print("\nDone! Thumbnails saved to photos/thumbs/")
