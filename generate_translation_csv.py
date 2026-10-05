import re
import shutil
import os
from dataclasses import dataclass
from tools import TranslationObject
from tools import to_sjis
from tools import scan_file
from tools import looks_japanese
from tools import write_to_file
from tools import save_to_csv



path = "./extracted/SLPS_021.17"
filename = os.path.basename(path)
if not os.path.exists(path + ".orig"):
    shutil.copy(path, path + ".orig")

data = bytearray(open(path, "rb").read())
start, end = 0x0000, 0x0000 # all 0's means search whole file





found_translations = scan_file(start, end, data)
kept_translations = []

for to in found_translations:
    if to.length > 4 and looks_japanese(to.text_original):
        kept_translations.append(to)
        
for to in kept_translations:
    to.print()


save_to_csv(kept_translations, f"{filename}_translations.csv")
print(f"Saved {len(kept_translations)} rows to {filename}_translations.csv")



