import pye57
from PIL import Image
import io
import os
import py360convert
import numpy as np
import csv

# E57 file path
e57 = pye57.E57("cloud_0.e57")

# open CSV files to write
f = open("skyboxes.csv", "w", newline="", encoding="utf-8")
csvSkyboxes = csv.writer(f)
csvSkyboxes.writerow(["Name", "j", "k", "pos X", "pos Y", "pos Z", "rot X", "rot Y", "rot Z", "rot W"])  # Header
f1 = open("panoramas.csv", "w", newline="", encoding="utf-8")
csvPanoramas = csv.writer(f1)
csvPanoramas.writerow(["Name", "j", "pos X", "pos Y", "pos Z", "rot X", "rot Y", "rot Z", "rot W"])  # Header

# Directories
skyboxes = "skyboxes"
panoramas = "panoramas"
os.makedirs(skyboxes, exist_ok=True)
os.makedirs(panoramas, exist_ok=True)

# Output size for equirectangular images
# Smaller images by default to reduce memory usage
# Full resolution can be set to 16384x8192, but it may require more memory and processing time
w = 4096
h = 2048

# Read images from E57 file
root = e57.image_file.root()
images2d = root["images2D"]

# Loop through each panorama (6 images per panorama)
for j in range(images2d.childCount() // 6):

    # Dictionary to hold the 6 faces of the cubemap
    faces = {}

    # Loop through each face of the cubemap (6 faces)
    for k in range(6):

        img_node = images2d[j * 6 + k]
        
        try:
            # Read the image data from the E57 file
            pinhole = img_node["pinholeRepresentation"]
            blob = pinhole["jpegImage"]

            # Read the image data into a byte array
            n_bytes = blob.byteCount()
            buf = bytearray(n_bytes)
            blob.read(buf, 0, n_bytes)

            # Convert the byte array to an image using PIL
            img = Image.open(io.BytesIO(buf))

            # Store the image in the faces dictionary with the corresponding face name
            face_names = ['U', 'F', 'R', 'B', 'L', 'D']
            faces[face_names[k]] = np.array(img)

            # Save the individual face image to the skyboxes directory
            name = img_node["name"].value()
            out_path = f"{skyboxes}/pano{j:02d}_{name}.jpg"
            img.save(out_path)
            print(f"Saved {out_path}")

            # write metadata to skyboxes CSV 
            position = img_node["pose"]["translation"]
            rotation = img_node["pose"]["rotation"]
            csvSkyboxes.writerow([   name, j, k,
                position['x'].value(), position['y'].value(), position['z'].value(),
                rotation['x'].value(), rotation['y'].value(), rotation['z'].value(), rotation['w'].value()
            ])

        except Exception as e:
            print(f"Failed on index {j * 6 + k}: {e}")

    if len(faces) != 6:
        print(f"Skipping panorama {j}: incomplete cubemap")
        continue

    # Convert the cubemap to equirectangular format and save it
    out_path = f"{panoramas}/pano{j:02d}.jpg"
    equirect = py360convert.c2e(faces, h, w, cube_format='dict')
    Image.fromarray(equirect.astype('uint8')).save(out_path)
    print(f"--> Saved {out_path}")

    # write metadata to skyboxes CSV
    # position should normally be shared by all 6 images, so we can just take the first image for the panorama
    # rotation will be taken from the last image, which represents down direction in the cubemap, which is usually the most relevant for equirectangular images
    name = f"pano{j:02d}"
    position = images2d[j * 6]["pose"]["translation"]
    rotation = images2d[j * 6 + 5]["pose"]["rotation"]
    csvPanoramas.writerow([   name, j,  
        position['x'].value(), position['y'].value(), position['z'].value(),
        rotation['x'].value(), rotation['y'].value(), rotation['z'].value(), rotation['w'].value()
    ])

# Close the CSV file
f.close()



