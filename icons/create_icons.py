#!/usr/bin/env python3
"""
Simple script to create placeholder icons for the Chrome extension
"""
from PIL import Image, ImageDraw, ImageFont

def create_icon(size, filename):
    """Create a simple icon with text"""
    # Create image with blue background
    img = Image.new('RGB', (size, size), color='#1a73e8')
    draw = ImageDraw.Draw(img)

    # Draw text
    text = "MD"

    # Try to use a nice font, fall back to default
    try:
        font_size = size // 2
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        font = ImageFont.load_default()

    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center text
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - bbox[1]

    # Draw white text
    draw.text((x, y), text, fill='white', font=font)

    # Save
    img.save(filename)
    print(f"Created {filename}")

if __name__ == '__main__':
    import os
    os.chdir(os.path.dirname(__file__))

    create_icon(16, 'icon16.png')
    create_icon(48, 'icon48.png')
    create_icon(128, 'icon128.png')

    print("\n✓ All icons created successfully!")
