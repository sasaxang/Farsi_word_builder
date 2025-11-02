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

def combine_affixes(prefix: str, root: str, suffix: str) -> str:
    word = root or ""

    if prefix:
        word = smart_join(prefix, word)

    if suffix:
        word = smart_join(word, suffix, is_suffix=True)

    return word
