# E57 Repository

This repository contains two simple Python scripts for working with E57 files.

## e57.py

This script analyses an E57 file (specify the filename in line 10) and extracts all the images into one folder (*skyboxes*) and the equirectangular panoramas into another (*panoramas*).

Additionally, a `skybox.csv` file is generated, containing useful metadata, particularly the position and rotation of each image.

The resolution of the equirectangular panoramas has been reduced to suit the current project requirements. This can easily be changed (see lines 23–27 in the script).

**Important assumption:** The script expects the images to follow a particular order:

- Image 0: top (up)
- Image 1: front
- Image 2: right
- Image 3: back
- Image 4: left
- Image 5: bottom (down)

This ordering works perfectly well with the scan I am using, but it may not be universal across all E57 files or scanning software. Adjustments may be necessary for other datasets.

## e57_xml.py

This script extracts the XML data from an E57 file, revealing its complete internal structure.

## Credits

Quite a bit of vibe programming was involved, with Claude, GPT, and a little help from Copilot!
