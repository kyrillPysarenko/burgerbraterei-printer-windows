import win32print
import win32ui
from PIL import Image, ImageWin, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import qrcode
from .print_service import print_image
import textwrap

def create_and_print_label(product_name, event_name, barcode_data, product_date,
                           storage_name, storage_shelf, storage_level, note, handler,
                           amount, unit, label_amount):
    # Create a new image
    printer_name = "Brother QL-700"

    hdc = win32ui.CreateDC()
    hdc.CreatePrinterDC(printer_name)
    width = hdc.GetDeviceCaps(110)  # PHYSICALWIDTH
    height = hdc.GetDeviceCaps(111)  # PHYSICALHEIGHT
    hdc.DeleteDC()

    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Load fonts
    title_font = ImageFont.truetype("arial.ttf", 40)
    font = ImageFont.truetype("arial.ttf", 34)
    small_font = ImageFont.truetype("arial.ttf", 18)
    #barcode_font = ImageFont.truetype("arial.ttf", 12)
    amount_font = ImageFont.truetype("arial.ttf", 28)

    # Function to draw wrapped text
    def draw_wrapped_text(text, position, font, max_width):
        x, y = position
        for line in textwrap.wrap(text, width=int(max_width / font.getlength("x"))):
            bbox = font.getbbox(line)
            draw.text((x, y), line, font=font, fill="black")
            y += bbox[3] - bbox[1]
        return y  # Return the new y position

    # Draw amount in top right corner if provided
    if amount is not None and unit is not None:
        amount_text = f"{amount} {unit}"
        amount_width = draw.textlength(amount_text, font=amount_font)
        draw.text((width - amount_width - 100, 10), amount_text, font=amount_font, fill="black")

    # Draw information
    y_position = 10
    y_position = draw_wrapped_text(f"{product_name}", (10, y_position), title_font, width - 180)
    y_position += 15  # Add some extra spacing after the product name

    if event_name:
        y_position = draw_wrapped_text(f"Event: {event_name}", (10, y_position), font, width - 20)
        y_position += 15

    y_position = draw_wrapped_text(f"{product_date}", (10, y_position), font, width - 20)
    y_position += 15
    y_position = draw_wrapped_text(f"{storage_name}", (10, y_position), font, width - 20)
    y_position += 15
    y_position = draw_wrapped_text(f"{storage_shelf}", (10, y_position), font, width - 20)
    y_position += 15
    y_position = draw_wrapped_text(f"{storage_level}", (10, y_position), font, width - 20)
    y_position += 15

    y_position = draw_wrapped_text("Hinweis:", (10, y_position), font, width - 20)
    y_position += 5
    y_position = draw_wrapped_text(note, (10, y_position), small_font, width - 20)
    y_position += 15
    y_position = draw_wrapped_text(f"Bearbeiter: {handler}", (10, y_position), font, width - 20)

    # Barcode or QR code logic remains the same
    if barcode_data.startswith("burgerbraterei"):
        # QR code logic...
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(barcode_data)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")

        qr_width, qr_height = qr_img.size
        scale_factor = min((width - 20) / qr_width, (height - y_position - 40) / qr_height)
        qr_img = qr_img.resize((int(qr_width * scale_factor), int(qr_height * scale_factor)), Image.Resampling.LANCZOS)

        qr_position = (10, height - qr_img.size[1] - 20)
        img.paste(qr_img, qr_position)

    else:
        # Barcode logic...
        barcode_class = barcode.get_barcode_class('code128')
        barcode_image = barcode_class(barcode_data, writer=ImageWriter())
        barcode_buffer = BytesIO()
        barcode_image.write(barcode_buffer)
        barcode_image = Image.open(barcode_buffer)

        barcode_width = width - 20
        barcode_height = min(200, height - y_position - 60)  # Adjust barcode height if needed

        resized_barcode = barcode_image.resize((barcode_width, barcode_height), Image.Resampling.LANCZOS)

        barcode_position = (10, height - barcode_height - 40)
        img.paste(resized_barcode, barcode_position)
    # Save the image
    img.save("label.png")

    # Print the image
    for _ in range(label_amount):
        print("Printing label...", _)
        print("amount on label", amount)
        print_image("label1.png")