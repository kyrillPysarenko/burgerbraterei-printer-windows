import os
from PIL import Image, ImageDraw, ImageFont
from brother_ql.backends.pyusb import BrotherQLBackendPyUSB
from brother_ql.raster import BrotherQLRaster
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send

# Create an image with text
text = "TEST"
font_size = 40
font = ImageFont.truetype("arial.ttf", font_size)  # Ensure you have the font file or use a default font
image = Image.new('RGB', (200, 100), color=(255, 255, 255))
draw = ImageDraw.Draw(image)
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]
draw.text(((200 - text_width) / 2, (100 - text_height) / 2), text, font=font, fill=(0, 0, 0))

# Convert the image to a raster file
qlr = BrotherQLRaster('QL-700')
instructions = convert(qlr, [image], '62')  # Pass the image as a list

# Initialize the pyusb backend with the USB path
usb_path = 'usb://0x04f9:0x2042'  # Replace with your actual USB path
backend = BrotherQLBackendPyUSB(device_specifier=usb_path)

# Print the raster file over USB
send(instructions=instructions, printer_identifier=None, backend=backend, blocking=True)

import usb.backend.libusb1
import usb.core

# Get the libusb backend
backend = usb.backend.libusb1.get_backend(find_library=lambda x: x)

# Find all USB devices
devices = usb.core.find(find_all=True, backend=backend)
for dev in devices:
    print(f"ID: {dev.idVendor}:{dev.idProduct}, Address: {dev.address}")

