import json
from utils.loader import load_affixes_json, load_affixes_excel, save_affixes_json

def persian_sort_key(word):
    """
    Custom sort key for Persian alphabet.
    Maps characters to their correct order:
    آ, ا, ب, پ, ت, ث, ج, چ, ح, خ, د, ذ, ر, ز, ژ, س, ش, ص, ض, ط, ظ, ع, غ, ف, ق, ک, گ, ل, م, ن, و, ه, ی
    """
    alphabet_order = {
        'آ': 0, 'ا': 1, 'ب': 2, 'پ': 3, 'ت': 4, 'ث': 5, 'ج': 6, 'چ': 7,
        'ح': 8, 'خ': 9, 'د': 10, 'ذ': 11, 'ر': 12, 'ز': 13, 'ژ': 14,
        'س': 15, 'ش': 16, 'ص': 17, 'ض': 18, 'ط': 19, 'ظ': 20, 'ع': 21,
        'غ': 22, 'ف': 23, 'ق': 24, 'ک': 25, 'گ': 26, 'ل': 27, 'م': 28,
        'ن': 29, 'و': 30, 'ه': 31, 'ی': 32, 'ي': 32, 'ك': 25  # Handle Arabic variants
    }
    
    return [alphabet_order.get(char, 100 + ord(char)) for char in word]

def load_affixes(path="data/affixes.json"):
    affixes = load_affixes_json(path)

    # ✅ Sort each list alphabetically using Persian sort key
    for key in ["prefixes", "roots", "suffixes"]:
        affixes[key] = sorted(affixes[key], key=persian_sort_key)

    return affixes

def save_affixes(path, affixes):
    # Ensure data is sorted before saving
    for key in ["prefixes", "roots", "suffixes"]:
        affixes[key] = sorted(affixes[key], key=persian_sort_key)
    save_affixes_json(path, affixes)

def merge_affixes(existing, new):
    for key in ["prefixes", "roots", "suffixes"]:
        existing[key].extend([item for item in new.get(key, []) if item not in existing[key]])
    
    # Sort after merging
    for key in ["prefixes", "roots", "suffixes"]:
        existing[key] = sorted(existing[key], key=persian_sort_key)
