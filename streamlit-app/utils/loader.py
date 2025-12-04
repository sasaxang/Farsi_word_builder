import json
import pandas as pd

def load_affixes_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_affixes_excel(path):
    df = pd.read_excel(path)
    return {
        "prefixes": df["prefixes"].dropna().tolist(),
        "roots": df["roots"].dropna().tolist(),
        "suffixes": df["suffixes"].dropna().tolist()
    }

def save_affixes_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
