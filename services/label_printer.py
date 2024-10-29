import win32print
import win32ui
from PIL import Image, ImageWin, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import qrcode
from .print_service import print_image
import textwrap
import os


def get_font(size, bold=False):
    """
    Load the specified font from the parent directory's fonts folder.
    """
    try:
        font_file = "Roboto-Bold.ttf" if bold else "Roboto-Regular.ttf"
        # Set the directory to the parent folder of the current file
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fonts_dir = os.path.join(parent_dir, 'fonts')
        font_path = os.path.join(fonts_dir, font_file)

        #print(f"Loading font from {font_path}")
        # Attempt to load the font
        font = ImageFont.truetype(font_path, size)
        #print(f"Successfully loaded font from {font_path}")
        return font
    except Exception as e:
        print(f"Error loading font from {font_path}: {e}")

        # Last resort: Use default PIL font and scale it
        default_font = ImageFont.load_default()
        scale_factor = size / 10
        return default_font.font_variant(size=int(scale_factor))


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

    current_dir = os.path.dirname(os.path.abspath(__file__))
    fonts_dir = os.path.join(current_dir, 'fonts')

    # Load fonts
    try:
        title_font = get_font(40, bold=True)
        font = get_font(34)
        small_font = get_font(18)
        amount_font = get_font(28)
    except Exception as e:
        print(f"Error loading fonts: {e}")
        # If all else fails, use emergency large default font
        from PIL import ImageFont
        base_font = ImageFont.load_default()
        title_font = base_font.font_variant(size=40)  # Will make it roughly 40px
        font = base_font.font_variant(size=3)  # Will make it roughly 30px
        small_font = base_font.font_variant(size=2)  # Will make it roughly 20px
        amount_font = base_font.font_variant(size=3)

    # Function to draw wrapped text
    def draw_wrapped_text(text, position, font, max_width, line_spacing=5):
        x, y = position
        avg_char_width = font.getlength("x") if font.getlength("x") > 0 else 10  # Fallback to 10 if getlength fails
        for line in textwrap.wrap(text, width=int(max_width / avg_char_width)):
            bbox = font.getbbox(line)
            draw.text((x, y), line, font=font, fill="black")
            y += bbox[3] - bbox[1] + line_spacing  # Add line_spacing to increase line spacing
        return y  # Return the new y position

    # Draw amount in top right corner if provided
    if amount is not None and unit is not None:
        amount_text = f"{amount} {unit}"
        amount_width = draw.textlength(amount_text, font=amount_font)
        draw.text((width - amount_width - 50, 10), amount_text, font=amount_font, fill="black")

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

        barcode_position = (10, height - barcode_height - 10)
        img.paste(resized_barcode, barcode_position)
    # Save the image
    img.save("label.png")

    # Print the image
    for _ in range(label_amount):
        print("Printing label...", _)
        print("amount on label", amount)
        print_image("label.png")