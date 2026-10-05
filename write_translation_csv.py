import re
import shutil
import os
import sys
from dataclasses import dataclass
from tools import TranslationObject, to_sjis, scan_file, looks_japanese, write_to_file, save_to_csv, load_from_csv, patch_entry


csv_to_load = "./SLPS_021.17_translations_new.csv"
path = "./extracted/SLPS_021.17"

if not os.path.exists(path + ".orig"):
    shutil.copy(path, path + ".orig")

# always start from the untouched original, so re-running never stacks old patches
data = bytearray(open(path + ".orig", "rb").read())
original_size = len(data)


translations = load_from_csv(csv_to_load)

to_write = [to for to in translations if len(to.text_new) >= 1]

print(f"{len(to_write)} entries have new text:\n")
for to in to_write:
    to.print()

tmp = input(f"\nWrite these {len(to_write)} translations from {csv_to_load} to {path} ? y/n: ")
if 'n' in tmp:
    sys.exit()

written = 0
skipped = 0

for to in to_write:
    if patch_entry(to, data):
        written += 1
    else:
        skipped += 1

if len(data) != original_size:
    print("ERROR: file size changed, nothing saved.")
    sys.exit()

with open(path, "wb") as f:
    f.write(data)

print(f"\nDone. Wrote {written} entries, skipped {skipped}.")
