from utils.loader import load_affixes_json, load_affixes_excel, save_affixes_json

def load_affixes(path):
    return load_affixes_json(path)

def save_affixes(path, affixes):
    save_affixes_json(path, affixes)

def merge_affixes(existing, new):
    for key in ["prefixes", "roots", "suffixes"]:
        existing[key].extend([item for item in new.get(key, []) if item not in existing[key]])
