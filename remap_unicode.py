import os
import json
from typing import Dict, Any
from fontTools.ttLib import TTFont

def remap_unicode(font_path: str, remap_config: Dict[str, Dict[str, str]]):
    print(f"Processing font: {font_path}")  # Debugging statement
    
    # Check if file is already remapped
    filename = os.path.basename(font_path)
    if '_remapped.' in filename:
        print(f"Skipping already remapped font: {filename}")
        return
        
    try:
        font = TTFont(font_path)
    except Exception as e:
        print(f"Failed to load font {font_path}: {e}")  # Error handling
        return  # Skip this font and continue with the next one

    cmap = font['cmap'].getcmap(3, 1).cmap  # Windows Unicode BMP (UCS-2)
    print(f"Original cmap: {cmap}")  # Debugging statement

    # Update this section to safely access the remap configuration
    if not isinstance(remap_config, dict) or 'remap' not in remap_config:
        print(f"Invalid remap configuration: {remap_config}")
        return
        
    for keyboard_unicode, font_unicode in remap_config['remap'].items():
        keyboard_unicode = int(keyboard_unicode, 16)
        font_unicode = int(font_unicode, 16)
        print(f"Remapping {hex(font_unicode)} to {hex(keyboard_unicode)}")  # Debugging statement
        if font_unicode in cmap:
            glyph_name = cmap[font_unicode]
            cmap[keyboard_unicode] = glyph_name
            print(f"Mapped {hex(font_unicode)} to {hex(keyboard_unicode)} with glyph name: {glyph_name}")  # Debugging statement
        else:
            print(f"Font unicode {hex(font_unicode)} not found in cmap")  # Debugging statement

    # Get the original file extension and create output path
    base, ext = os.path.splitext(font_path)
    output_path = f"{base}_remapped{ext}"
    
    # Save in the original format
    try:
        font.save(output_path)
        print(f"Saved remapped font to {output_path}")  # Debugging statement
    except Exception as e:
        print(f"Failed to save font {output_path}: {e}")  # Error handling

def process_fonts(config: Dict[str, Any]):
    print(f"Processing fonts...")
    # Update this section to safely handle the remap configuration
    if not isinstance(config, dict):
        print("Invalid configuration format")
        return
        
    remap_dict = {'remap': config.get('remap', {})}  # Wrap in expected structure
    skip_eot = config.get('skip_eot', False)
    
    # Ensure fonts directory exists
    fonts_dir = os.path.join(os.path.dirname(__file__), 'fonts')
    if not os.path.exists(fonts_dir):
        os.makedirs(fonts_dir)
    
    # Handle folder path within fonts directory
    if 'folder_path' in config:
        folder_path = os.path.join(fonts_dir, config['folder_path'])
        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                if skip_eot and filename.endswith('.eot'):
                    print(f"Skipping EOT file: {filename}")
                    continue
                    
                full_path = os.path.join(folder_path, filename)
                if os.path.isfile(full_path):
                    remap_unicode(full_path, remap_dict)
        else:
            print(f"Folder not found in fonts directory: {folder_path}")
    
    # Handle individual files within fonts directory
    if 'files' in config:
        for filename in config['files']:
            full_path = os.path.join(fonts_dir, filename)
            if skip_eot and filename.endswith('.eot'):
                print(f"Skipping EOT file: {filename}")
                continue
                
            if os.path.exists(full_path):
                remap_unicode(full_path, remap_dict)
            else:
                print(f"File not found in fonts directory: {filename}")

if __name__ == '__main__':
    try:
        with open('remap_config.json', 'r') as f:
            config = json.load(f)
        process_fonts(config)
    except Exception as e:
        print(f"Error processing fonts: {e}")
