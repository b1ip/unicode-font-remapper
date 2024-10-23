# Unicode Font Remapping Tool

A tool for remapping Unicode characters in font files. This tool consists of two parts:

1. A web interface for creating remapping configurations
2. A Python script for processing font files

## Dependencies

### Python Dependencies

 ```bash
pip install fonttools
pip install brotli # Required for WOFF2 support
 ```

## Usage

1. **Prepare Font Files**
   - Place all font files in the `fonts` directory of the project
   - You can organize fonts in subfolders within the `fonts` directory

2. **Generate Configuration**
   - Open `remap_unicode.html` in a web browser
   - Choose one of the following options:
     - **Select Subfolder**: Enter the name of a subfolder within the `fonts` directory
     - **Select Files**: Choose individual files from the `fonts` directory
   - Add character remapping pairs:
     - Enter the keyboard character you want to type
     - Enter the font character you want it to display
   - Choose whether to skip EOT files
   - Click "Generate Configuration"
   - Download the generated `remap_config.json`

3. **Process Fonts**

   - Place the downloaded `remap_config.json` in the project root directory
   - Run the script:

   ```bash
   python remap_unicode.py
   ```

   - Processed fonts will be saved with '_remapped' suffix in their original location

## Configuration Format

The `remap_config.json` supports two formats:

1. **Subfolder Format**:

```json
{
    "remap": {
        "0x21b": "0x163"
    },
    "folder_path": "font_set",
    "skip_eot": true
}
```

2. **Individual Files Format**:

```json
{
    "remap": {
        "0x21b": "0x163"
    },
    "files": [
        "font1.ttf",
        "font2.woff"
    ],
    "skip_eot": true
}
```

## File Structure

 ```bash
# Start of Selection
project/
├── remap_unicode.html
├── remap_unicode.py
├── remap_config.json
└── fonts/
    ├── font_set/
    ├── font1.ttf
    ├── font2.woff
    └── ...
# End of Selection
 ```

## Supported Font Formats

- TrueType Font (.ttf)
- OpenType Font (.otf)
- Web Open Font Format (.woff)
- Web Open Font Format 2 (.woff2)
- Embedded OpenType (.eot)

## Notes

- Processed fonts are saved with '_remapped' suffix
- Files containing '_remapped' in their name are skipped
- The tool preserves the original font format
- Make backups of your font files before processing
