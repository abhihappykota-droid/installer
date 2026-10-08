#!/usr/bin/env python3
"""
Create Prynt icon (.ico) from logo PNG
Run this on Windows before building the installer.
"""

from PIL import Image
import sys
from pathlib import Path

def create_icon():
    """Convert PNG logo to .ico file with multiple sizes."""
    
    # Find logo
    logo_path = Path(__file__).parent.parent / 'frontend' / 'public' / 'prynt-logo.png'
    
    if not logo_path.exists():
        print(f"❌ Logo not found at: {logo_path}")
        print("\nPlease ensure prynt-logo.png exists in frontend/public/")
        sys.exit(1)
    
    print(f"✓ Found logo: {logo_path}")
    
    # Load image
    try:
        img = Image.open(logo_path)
        print(f"✓ Loaded image: {img.size[0]}x{img.size[1]} pixels")
    except Exception as e:
        print(f"❌ Failed to load image: {e}")
        sys.exit(1)
    
    # Convert to RGBA if needed
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
        print("✓ Converted to RGBA")
    
    # Create icon with multiple sizes
    # Windows needs 16x16, 32x32, 48x48, 256x256
    icon_sizes = [(16, 16), (32, 32), (48, 48), (256, 256)]
    
    output_path = Path(__file__).parent / 'prynt_icon.ico'
    
    try:
        img.save(
            output_path,
            format='ICO',
            sizes=icon_sizes
        )
        print(f"✓ Created icon: {output_path}")
        print(f"  Sizes: {', '.join([f'{w}x{h}' for w, h in icon_sizes])}")
        print("\n✅ Icon created successfully!")
        print("\nNext step: Run 'python build_installer.py' to build .exe with icon")
        
    except Exception as e:
        print(f"❌ Failed to create icon: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 60)
    print("Prynt Icon Creator")
    print("=" * 60)
    print()
    
    # Check if PIL/Pillow is installed
    try:
        from PIL import Image
    except ImportError:
        print("❌ Pillow not installed!")
        print("\nInstall it with:")
        print("  pip install Pillow")
        sys.exit(1)
    
    create_icon()
