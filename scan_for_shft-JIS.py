path = "./extracted/SPRIGGAN/SPRIGGAN.M"
data = open(path, "rb").read()

MIN_CHARS = 3   # ignore runs shorter than this many characters

def is_lead(b):
    return 0x81 <= b <= 0x9F or 0xE0 <= b <= 0xFC

def is_trail(b):
    return 0x40 <= b <= 0x7E or 0x80 <= b <= 0xFC


def looks_japanese(s):
    kana = sum("\u3040" <= c <= "\u30ff" for c in s)
    return kana >= 2 or (kana >= 1 and len(s) >= 4)

def scan(data):
    results = []
    i, n = 0, len(data)
    start = None
    text = []
    has_double = False

    def flush(end):
        nonlocal start, text, has_double
        if start is not None and has_double and len(text) >= MIN_CHARS:
            results.append((start, end - start, "".join(text)))
        start, text, has_double = None, [], False

    while i < n:
        b = data[i]
        # double-byte character
        if is_lead(b) and i + 1 < n and is_trail(data[i + 1]):
            try:
                ch = data[i:i + 2].decode("shift_jis")
            except UnicodeDecodeError:
                flush(i)
                i += 1
                continue
            if start is None:
                start = i
            text.append(ch)
            has_double = True
            i += 2
        # printable ASCII (kept inside a run, e.g. "/" or "%s")
        elif 0x20 <= b <= 0x7E:
            if start is None:
                start = i
            text.append(chr(b))
            i += 1
        # anything else ends the run (00, control bytes, binary data)
        else:
            flush(i)
            i += 1
    flush(n)
    return results

for off, length, s in scan(data):
    if looks_japanese(s):
        print(f"{off:#08x} len={length:4d}  {s}")