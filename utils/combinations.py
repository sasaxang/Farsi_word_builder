def calculate_total_combinations(affixes, structure):
    """
    Calculate the total number of possible combinations based on the selected structure.
    Takes into account exclusion rules like 'انه' suffix not coming after roots ending in 'ه', 'ا', or 'آ'.
    
    Args:
        affixes: Dictionary containing 'prefixes', 'roots', and 'suffixes' lists
        structure: The selected word structure string
        
    Returns:
        Total number of valid combinations
    """
    prefixes = affixes.get("prefixes", [])
    roots = affixes.get("roots", [])
    suffixes = affixes.get("suffixes", [])
    
    # Determine which components are included based on structure
    include_prefix = structure in [
        "پیشوند + ریشه (مثل: بی‌گربه)", 
        "پیشوند + ریشه + پسوند (مثل: خویش‌گربه‌پرداز)", 
        "Prefix + Root (e.g. بی‌گربه)", 
        "Prefix + Root + Suffix (e.g. خویش‌گربه‌پرداز)"
    ]
    include_suffix = structure in [
        "ریشه + پسوند (مثل: گربه‌گاه)", 
        "پیشوند + ریشه + پسوند (مثل: خویش‌گربه‌پرداز)", 
        "Root + Suffix (e.g. گربه‌گاه)", 
        "Prefix + Root + Suffix (e.g. خویش‌گربه‌پرداز)"
    ]
    
    # Count roots that end in 'ه' (but not 'اه'), 'ا', or 'آ'
    problematic_roots = [r for r in roots if (
        (r.endswith("ه") and not r.endswith("اه")) or 
        r.endswith("ا") or 
        r.endswith("آ")
    )]
    normal_roots = [r for r in roots if r not in problematic_roots]
    
    # Check if 'انه' is in suffixes
    has_aneh = "انه" in suffixes
    
    if not include_prefix and not include_suffix:
        # Only root
        return len(roots)
    elif include_prefix and not include_suffix:
        # Prefix + Root
        # Add 1 to prefixes to account for empty prefix option
        return (len(prefixes) + 1) * len(roots)
    elif not include_prefix and include_suffix:
        # Root + Suffix
        # Add 1 to suffixes to account for empty suffix option
        if has_aneh:
            # For 'انه' suffix: only normal roots can use it
            # For other suffixes: all roots can use them
            aneh_combinations = len(normal_roots)  # انه with normal roots only
            other_suffix_combinations = (len(suffixes) - 1 + 1) * len(roots)  # other suffixes + empty with all roots
            return aneh_combinations + other_suffix_combinations
        else:
            return (len(suffixes) + 1) * len(roots)
    else:
        # Prefix + Root + Suffix
        # Add 1 to prefixes and suffixes to account for empty options
        if has_aneh:
            # Calculate combinations with 'انه' (only normal roots)
            aneh_combinations = (len(prefixes) + 1) * len(normal_roots)
            
            # Calculate combinations with other suffixes (all roots)
            other_suffix_combinations = (len(prefixes) + 1) * len(roots) * (len(suffixes) - 1 + 1)
            
            return aneh_combinations + other_suffix_combinations
        else:
            return (len(prefixes) + 1) * len(roots) * (len(suffixes) + 1)


def convert_to_persian_numerals(number):
    """Convert English numerals to Persian numerals."""
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    
    number_str = str(number)
    result = ''
    for char in number_str:
        if char in english_digits:
            result += persian_digits[english_digits.index(char)]
        else:
            result += char
    return result
