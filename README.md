# Spriggan Lunar Verse Translation

This repo contains the tools I wrote to help me translate Spriggan Lunar Verse, as well as the final patch itself. I also used jpsxdec to export/import some images and GIMP to edit and translate them.


## How to use the Patch
This is also included in the readme in the release

MD5SUM of "Spriggan - Lunar Verse (Japan).bin" = `173d741ec9483c87e20085a0f9b4098a`


- Get xdelta3 to apply patch

- Ensure your Spriggan Lunar Verse .bin file has the same hash as mine. If not go find one that does

- Run this command: `xdelta3 -d -s "Spriggan - Lunar Verse (Japan).bin" "Spriggan_EN.xdelta" "Spriggan - Lunar Verse (En).bin"` this will make a new bin file with patch applied.

- .cue files are just text, either copy and edit the .cue file to point to this new filename, or change the filename of our new .bin file to be what was previously there

- Play game

