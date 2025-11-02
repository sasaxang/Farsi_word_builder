from utils.zwnj_rules import no_zwj_after

def smart_join(part1: str, part2: str) -> str:
    """
    Joins two parts with ZWJ if needed.
    """
    if not part1 or not part2:
        return part1 + part2

    last = part1[-1]
    zwj = "\u200c"

    if last in no_zwj_after:
        return part1 + part2
    else:
        return part1 + zwj + part2

def combine_affixes(prefix, root, suffix):
    word = smart_join(prefix, root)
    word = smart_join(word, suffix)
    return word
