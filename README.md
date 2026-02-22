# EcoPrint

A desktop utility to rebalance PDF color distribution for printer ink management.

## Overview
The script processes PDF documents by remapping specific color ranges to a target hue. Black text is preserved and remains selectable in the output document. This tool is designed for users who want to balance the usage of various ink cartridges (e.g., shifting usage from Magenta/Cyan to Yellow) while maintaining document legibility.

## Features
- Hardware-independent PDF color remapping.
- Preservation of black text integrity.
- Selectable and searchable output PDF layer.
- Minimalist interface for file and profile selection.
- Native system dark/light mode support.

## Requirements
- Python 3.x
- PyMuPDF (fitz)
- Pillow
- pywebview

## Usage
Run the main script to launch the interface:

```bash
python color_swapper.py
```

1. Select a source PDF document.
2. Select an ink balance profile (Yellow, Red, or Blue base).
3. Execute the process.

The resulting file will be saved in the same directory as the source document with an "ecoprint_" prefix.

## Technical Notes
Documents are processed page-by-page using a high-resolution rasterization method for color accuracy, followed by an invisible text overlay to maintain searchability.
