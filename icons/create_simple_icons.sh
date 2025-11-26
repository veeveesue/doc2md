#!/bin/bash

# Create simple colored PNG icons using ImageMagick or sips (macOS)

cd "$(dirname "$0")"

# Function to create icon
create_icon() {
    size=$1
    filename=$2

    # Try using sips (macOS built-in)
    if command -v sips &> /dev/null; then
        # Create a temporary blue square
        python3 -c "
import base64
# Simple 1x1 blue pixel PNG
blue_png = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==')
with open('temp.png', 'wb') as f:
    f.write(blue_png)
"
        # Resize to desired size
        sips -z $size $size temp.png --out $filename &> /dev/null
        rm -f temp.png
        echo "Created $filename using sips"
    else
        # Fallback: create using Python without PIL
        python3 -c "
# Create a simple PNG file programmatically
def create_simple_png(size, filename, color_hex):
    import zlib
    import struct

    # Convert hex color to RGB
    color = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))

    # Create image data (RGB format)
    raw_data = b''
    for y in range(size):
        raw_data += b'\\x00'  # Filter type
        for x in range(size):
            raw_data += bytes(color)

    # Compress
    compressed = zlib.compress(raw_data)

    # PNG signature
    png = b'\\x89PNG\\r\\n\\x1a\\n'

    # IHDR chunk
    ihdr = struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0)
    png += struct.pack('>I', 13) + b'IHDR' + ihdr
    png += struct.pack('>I', zlib.crc32(b'IHDR' + ihdr))

    # IDAT chunk
    png += struct.pack('>I', len(compressed)) + b'IDAT' + compressed
    png += struct.pack('>I', zlib.crc32(b'IDAT' + compressed))

    # IEND chunk
    png += struct.pack('>I', 0) + b'IEND'
    png += struct.pack('>I', zlib.crc32(b'IEND'))

    with open(filename, 'wb') as f:
        f.write(png)

create_simple_png($size, '$filename', '1a73e8')
print('Created $filename using Python')
"
    fi
}

# Create icons
create_icon 16 icon16.png
create_icon 48 icon48.png
create_icon 128 icon128.png

echo ""
echo "✓ All icons created successfully!"
