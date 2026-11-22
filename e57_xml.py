
import struct
from pathlib import Path

source = Path("cloud_0.e57")
destination = source.with_suffix(".xml")

with open(source, "rb") as f:
    # Read the 48-byte E57 header
    header = f.read(48)
    signature, major, minor, file_length, xml_offset, xml_length, page_size = \
        struct.unpack("<8sIIQQQQ", header)

    print(f"Signature: {signature}, Version: {major}.{minor}, File Length: {file_length}, XML Offset: {xml_offset}, XML Length: {xml_length}, Page Size: {page_size}") 

    if signature != b"ASTM-E57" or page_size != 1024:
        raise ValueError("Invalid or unsupported E57 file")

    # Seek to the XML section
    f.seek(xml_offset)

    xml = bytearray()
    remaining = xml_length

    while remaining > 0:
        # Skip the 4-byte checksum at the end of each page
        position = f.tell() % page_size
        available = page_size - 4 - position

        if available <= 0:
            f.seek(page_size - position, 1)
            continue

        chunk = f.read(min(available, remaining))
        if not chunk:
            raise EOFError("Unexpected end of E57 file")

        xml.extend(chunk)
        remaining -= len(chunk)

with open(destination, "wb") as f:
    f.write(xml)

print(f"Saved {destination}")
