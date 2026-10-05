import re
import shutil
import os
import csv
from dataclasses import dataclass


@dataclass
class TranslationObject:
    id: int
    offset: int
    length: int
    text_original: str
    text_new: str

    def print(self):
        print(f"id: {self.id}, offset: {self.offset:#06x} len={self.length:3d}  Original: {self.text_original} || New: {self.text_new}, new_len={len(self.text_new)}")




KEEP_ASCII = re.compile(r"(/|%\d*[sdxX]|\(\d+\)|<\d+>|#|&|\*)")
#KEEP_ASCII = re.compile(r"(/|%\d*[sdxX])")



def to_sjis(text: str) -> bytes:
    """Encode English as full-width Shift-JIS, leaving control codes alone."""
    out = b""
    for part in KEEP_ASCII.split(text):
        if not part:
            continue
        if KEEP_ASCII.fullmatch(part):
            out += part.encode("ascii")
            continue
        for c in part:
            if c == " ":
                out += b"\x81\x40"                    # full-width space
            elif "!" <= c <= "~":
                out += chr(ord(c) + 0xFEE0).encode("cp932")   # full-width Latin
            else:
                out += c.encode("cp932")              # kana/kanji pass through
    return out

# def looks_japanese(s):
#     kana = sum("\u3040" <= c <= "\u30ff" for c in s)
#     return kana >= 2 or (kana >= 1 and len(s) >= 4)

def looks_japanese(s):
    kana = sum("\u3040" <= c <= "\u30ff" for c in s)
    kanji = sum("\u4e00" <= c <= "\u9fff" for c in s)
    return kana >= 2 or (kanji >= 4 and kana >= 1) or kanji / max(len(s), 1) > 0.6

def write_to_file(to: TranslationObject, data: bytearray, path):
    if not to.text_new:
        print("No new text set for this entry.")
        return
    raw = to_sjis(to.text_new)
    if len(raw) > to.length:
        print(f"Too long: {len(raw)} bytes, slot is {to.length} bytes. Not written.")
        tmp = input("Do you want to write anyway? y/n: ")
        if 'n' in tmp:
            return
    padded = raw + b"\x00" * (to.length - len(raw))   # overwrite old bytes with zeros
    data[to.offset:to.offset + to.length] = padded
    with open(path, "wb") as f:
        f.write(data)
    print(f"Wrote {len(raw)} bytes at {to.offset:#06x} (slot {to.length}).")
    print("Bytes:", raw.hex(" "))


def scan_file(start: int, end: int, data: bytearray):
    if end == 0:
        end = len(data)

    found = []
    pos = start
    id_it = 1
    while pos < end:
        nul = data.find(b"\x00", pos, end)
        if nul == -1:
            nul = end
        raw = data[pos:nul]
        if raw:
            try:
                text = raw.decode("shift_jis")
                length = len(raw)

                tmp = TranslationObject(id_it, pos, length, text, "")
                found.append(tmp)
                id_it += 1
            except UnicodeDecodeError:
                pass
        pos = nul + 1

    return found



def save_to_csv(translations, filename):
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        # header row
        writer.writerow(["id", "offset", "length", "text_original", "text_new"])

        # one row per entry
        for to in translations:
            writer.writerow([
                to.id,
                f"{to.offset:#x}",    # saved as text like 0x1178
                to.length,
                to.text_original,
                to.text_new,
            ])


def load_from_csv(filename):
    translations = []
    with open(filename, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            translations.append(TranslationObject(
                id=int(row["id"]),
                offset=int(row["offset"], 16),    # turns "0x1178" back into a number
                length=int(row["length"]),
                text_original=row["text_original"],
                text_new=row["text_new"],
            ))
    return translations




def patch_entry(to: TranslationObject, data: bytearray):
    """Put one translation into data (in memory only). Returns True if it was written."""
    if len(to.text_new) < 1:
        return False

    raw = to_sjis(to.text_new)

    if len(raw) > to.length:
        print(f"SKIPPED id {to.id} at {to.offset:#x}: {len(raw)} bytes, slot is {to.length}")
        return False

    padded = raw + b"\x00" * (to.length - len(raw))
    data[to.offset:to.offset + to.length] = padded
    return True