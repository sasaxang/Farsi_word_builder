from core.affix_manager import load_affixes, save_affixes, persian_sort_key

def verify_sorting():
    print("Loading affixes...")
    # This will load and sort them in memory
    affixes = load_affixes("data/affixes.json")
    
    prefixes = affixes["prefixes"]
    roots = affixes["roots"]
    suffixes = affixes["suffixes"]
    
    print("Verifying Prefix Order...")
    # Check 'پ' (Pe) vs 'ت' (Te) - Pe should be before Te
    # Check 'ب' (Be) vs 'پ' (Pe) - Be should be before Pe
    
    # Let's just print the sorted lists to visually confirm in logs and check specific known issues
    print(f"Prefixes: {prefixes}")
    
    # Automated check for specific characters if they exist
    try:
        idx_be = next(i for i, w in enumerate(prefixes) if w.startswith("بی"))
        idx_pe = next(i for i, w in enumerate(prefixes) if w.startswith("پ"))
        
        if idx_be < idx_pe:
            print("✅ PASS: 'بی' comes before 'پ...'")
        else:
            print("❌ FAIL: 'بی' comes after 'پ...'")
            
    except StopIteration:
        print("⚠️ Could not find examples for Be/Pe check in prefixes")

    print("Saving affixes to enforce sort in file...")
    save_affixes("data/affixes.json", affixes)
    print("Done.")

if __name__ == "__main__":
    verify_sorting()
