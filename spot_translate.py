import re
import shutil
import os
from dataclasses import dataclass
from tools import TranslationObject, to_sjis, scan_file, looks_japanese, write_to_file




path = "./extracted/SPRIGGAN/SPRIGGAN.M"
if not os.path.exists(path + ".orig"):
    shutil.copy(path, path + ".orig")

data = bytearray(open(path, "rb").read())
start, end = 0x0000, 0x147228c  # adjust the end to where the text stops




while True:
    found_translation = scan_file(start, end, data)

    for to in found_translation:
        if to.length > 10 and looks_japanese(to.text_original):
            to.print()
            

    picked_translation = int(input("Enter ID of object you want to edit: "))
    current_to: TranslationObject
    if picked_translation:
        for to in found_translation:
            if to.id == picked_translation:
                current_to = to

    print("\n You picked:\n\n")
    current_to.print()
    print("\n")



    while True:
        menu = int(input("Pick an action:\n 0. Back\n 1. Edit New Text\n 99. Write new text to file\nYour Choice: "))

        if menu == 1:
            new_text = input("Enter New Text: ")
            current_to.text_new = new_text
            print("\n")
            current_to.print()
        if menu == 0:
            break
        if menu == 99:
            write_to_file(current_to, data, path)
            break

    tmp = input("\n Do another? y/n")
    if "n" in tmp:
        break





