# User Guides - README

## Overview

This directory contains comprehensive user guides for the Farsi Word Builder application in both Farsi and English.

## Files

### User Guides
- **`user_guide_fa.md`** - Complete Farsi user guide (راهنمای فارسی)
- **`user_guide_en.md`** - Complete English user guide

### Supporting Files
- **`screenshot_checklist.md`** - Checklist for capturing required screenshots
- **`screenshots/`** - Directory for storing screenshot images

## Screenshot Requirements

The guides reference 10 screenshots for each language (20 total). Use the `screenshot_checklist.md` to capture all required images.

### To Capture Screenshots:

1. Open the application at http://localhost:8501
2. Follow the checklist in `screenshot_checklist.md`
3. Save screenshots to the `screenshots/` directory with exact filenames
4. Screenshots will automatically appear in the guides

## Exporting to PDF

To convert the markdown guides to PDF:

### Option 1: Using Pandoc (Recommended)
```bash
# Install pandoc if not already installed
sudo apt-get install pandoc texlive-xetex

# Convert Farsi guide (with RTL support)
pandoc user_guide_fa.md -o user_guide_fa.pdf --pdf-engine=xelatex -V mainfont="Vazir"

# Convert English guide
pandoc user_guide_en.md -o user_guide_en.pdf --pdf-engine=xelatex
```

### Option 2: Using Online Tools
- Upload the markdown file to https://www.markdowntopdf.com/
- Or use https://dillinger.io/ (supports export to PDF)

### Option 3: Using VS Code Extension
- Install "Markdown PDF" extension
- Right-click on the markdown file → "Markdown PDF: Export (pdf)"

## Guide Features

✅ Comprehensive coverage of all features  
✅ Step-by-step instructions with screenshots  
✅ Color-coded sections for easy navigation  
✅ Examples and practical tips  
✅ Troubleshooting section  
✅ Beginner-friendly language  

## Customization

The guides use inline HTML/CSS for styling. When exporting to PDF:
- Some styling may not be preserved
- Consider using CSS files for better PDF export
- Test the PDF output and adjust as needed

## Adding Screen Recordings

To add screen recordings (mentioned in the guides):

1. Record videos using OBS Studio, QuickTime, or similar
2. Save as `.mp4` or `.webm` format
3. Upload to a hosting service (YouTube, Vimeo, etc.)
4. Add links in the markdown files where indicated

## Maintenance

When updating the application:
- Update relevant sections in both guides
- Re-capture affected screenshots
- Update version numbers and dates
- Test PDF export after changes
