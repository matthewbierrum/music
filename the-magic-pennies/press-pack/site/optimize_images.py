#!/usr/bin/env python3
"""
Image optimization script for The Magic Pennies EPK
Creates WebP thumbnails for the gallery and optimizes the hero image
"""

from PIL import Image
import os
from pathlib import Path

SITE_DIR = Path(__file__).parent
PHOTOS_DIR = SITE_DIR / "photos"
THUMBS_DIR = SITE_DIR / "photos" / "thumbs"

# Thumbnail settings
THUMB_MAX_WIDTH = 600
THUMB_QUALITY = 85

# Hero image settings  
HERO_MAX_WIDTH = 1920
HERO_QUALITY = 80

def create_thumbnail(input_path: Path, output_path: Path, max_width: int, quality: int):
    """Create an optimized WebP thumbnail"""
    with Image.open(input_path) as img:
        # Convert to RGB if necessary (for PNG with transparency)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Calculate new dimensions maintaining aspect ratio
        ratio = max_width / img.width
        if ratio < 1:  # Only resize if larger than max
            new_size = (max_width, int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)
        
        # Save as WebP
        img.save(output_path, 'WEBP', quality=quality, method=6)
        
    original_size = input_path.stat().st_size / 1024 / 1024
    new_size = output_path.stat().st_size / 1024 / 1024
    print(f"  {input_path.name}: {original_size:.2f}MB -> {new_size:.2f}MB ({(1-new_size/original_size)*100:.0f}% reduction)")

def optimize_hero():
    """Optimize the hero background image"""
    hero_path = SITE_DIR / "background-image-wide.jpg"
    hero_webp = SITE_DIR / "background-image-wide.webp"
    
    if hero_path.exists():
        print("\nOptimizing hero image...")
        with Image.open(hero_path) as img:
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            ratio = HERO_MAX_WIDTH / img.width
            if ratio < 1:
                new_size = (HERO_MAX_WIDTH, int(img.height * ratio))
                img = img.resize(new_size, Image.LANCZOS)
            
            img.save(hero_webp, 'WEBP', quality=HERO_QUALITY, method=6)
        
        original_size = hero_path.stat().st_size / 1024 / 1024
        new_size = hero_webp.stat().st_size / 1024 / 1024
        print(f"  Hero: {original_size:.2f}MB -> {new_size:.2f}MB ({(1-new_size/original_size)*100:.0f}% reduction)")

def main():
    # Create thumbs directory
    THUMBS_DIR.mkdir(exist_ok=True)
    
    print("Creating optimized thumbnails...")
    
    # Process each photo
    for photo in PHOTOS_DIR.iterdir():
        if photo.is_file() and photo.suffix.lower() in ('.jpg', '.jpeg', '.png'):
            # Create WebP thumbnail with sanitized filename
            thumb_name = photo.stem.replace(' ', '-').replace('.', '') + '.webp'
            thumb_path = THUMBS_DIR / thumb_name
            create_thumbnail(photo, thumb_path, THUMB_MAX_WIDTH, THUMB_QUALITY)
    
    # Optimize hero image
    optimize_hero()
    
    print("\n✅ Optimization complete!")
    print(f"Thumbnails saved to: {THUMBS_DIR}")

if __name__ == "__main__":
    main()
