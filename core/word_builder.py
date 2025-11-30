from utils.zwnj_rules import no_zwj_after

NO_ZWJ_SUFFIXES = ["انه", "ی"]  # پسوندهایی که بدون ZWJ به ریشه می‌چسبند

def smart_join(part1: str, part2: str, is_suffix=False) -> str:
    """
    Joins two parts with ZWJ if needed.
    - If part2 is a suffix in NO_ZWJ_SUFFIXES, skip ZWJ.
    - If part1 ends with a char in no_zwj_after, skip ZWJ.
    """
    if not part1 or not part2:
        return part1 + part2

    zwj = "\u200c"

    if is_suffix and part2 in NO_ZWJ_SUFFIXES:
        return part1 + part2

    last = part1[-1]
    if last in no_zwj_after:
        return part1 + part2
    else:
        return part1 + zwj + part2

def apply_nominal_form(word: str, last_part: str = "") -> str:
    """
    Applies nominal form suffix based on the last letter of the word.
    - Ends in 'ا' or 'و' -> append 'یی'
    - Ends in 'ه':
        - If ends in 'اه' (like گاه, خواه) -> append 'ی'
        - If last_part is 'ده' (like ده) -> append 'ی'
        - Otherwise -> append ZWNJ + 'ای'
    - Otherwise -> append 'ی'
    """
    if not word:
        return word
        
    last_char = word[-1]
    zwj = "\u200c"
    
    if last_char in ['ا', 'و']:
        return word + "یی"
    elif last_char == 'ه':
        # Exceptions for 'ه'
        if word.endswith("اه"):
            return word + "ی"
        elif last_part == "ده":
            return word + "ی"
        else:
            return word + zwj + "ای"
    else:
        return word + "ی"

def combine_affixes(prefix: str, root: str, suffix: str, is_nominal: bool = False) -> str:
    word = root or ""

    if prefix:
        word = smart_join(prefix, word)

    if suffix:
        word = smart_join(word, suffix, is_suffix=True)
        
    if is_nominal:
        # Determine the last part added (suffix if present, else root)
        last_part = suffix if suffix else root
        word = apply_nominal_form(word, last_part)

    return word
