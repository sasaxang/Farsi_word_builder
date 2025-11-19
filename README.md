# Farsi Word Builder

Farsi Word Builder is a playful and educational Streamlit app that generates random Persian (Farsi) words by combining prefixes, roots, and suffixes from a customizable affix bank. It is designed for language learners, writers, and creative developers who want to explore Persian word formation in an interactive way.

## Purpose

This tool can be used for:
- Vocabulary building and language learning
- Creative writing and storytelling
- Game or app development with Persian wordplay
- Linguistic experimentation and research

## Features

- Slot-machine-style word generator
- **Bilingual Support**: Interface available in both Persian (Farsi) and English
- Add new affixes (prefixes, roots, suffixes) directly from the UI
- Upload affix banks via Excel or JSON files
- Persistent storage in a local JSON file
- Simple and intuitive interface built with Streamlit

## Live App
You can try Farsi Word Builder directly in your browser via Streamlit:

🔗 https://farsiwordbuilder.streamlit.app/ No installation required—just open the link and start building words interactively.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/farsi-word-builder.git
cd farsi-word-builder
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run main.py
```

## File Structure

```
farsi-word-builder/
├── core/
│   ├── __init__.py
│   ├── affix_manager.py
│   ├── ui_components.py
│   └── word_builder.py
├── data/
│   ├── affixes.json        # Default affix bank
│   └── sample_affixes.xlsx # Sample Excel file for upload
├── utils/
│   ├── loader.py           # Utility functions for loading/saving affixes
│   └── zwnj_rules.py       # Zero-width non-joiner rules
├── app_en.py               # English version of the app
├── app_fa.py               # Farsi version of the app
├── main.py                 # Entry point / Language selector
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Upload Format

You can upload affix banks in either `.json` or `.xlsx` format.

### JSON format:

```json
{
  "prefixes": ["نا", "بی", "هم"],
  "roots": ["دان", "کار", "آگاه"],
  "suffixes": ["مند", "گر", "ی"]
}
```

## Usage

- Click the "Spin" button to generate a random word.
- Add new affixes using the form provided in the UI.
- Upload a `.json` or `.xlsx` file to import additional affixes.
- All changes are saved to the local `affixes.json` file.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome. You can:
- Fork the repository
- Submit pull requests
- Suggest new features or improvements

Please make sure your code is clean and documented before submitting.

## Author

Developed by Sasan — professional English-Farsi translator, localization expert, and creative developer.
