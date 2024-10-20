import win32print
import win32ui
from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from .print_service import print_image

def create_and_print_label(product_name, event_name, barcode_data, product_date,
                           storage_name, storage_shelf, storage_level, note, handler):
    # Erstelle ein neues Bild
    printer_name = win32print.GetDefaultPrinter()
    hdc = win32ui.CreateDC()
    hdc.CreatePrinterDC(printer_name)
    width = hdc.GetDeviceCaps(110)  # PHYSICALWIDTH
    height = hdc.GetDeviceCaps(111)  # PHYSICALHEIGHT
    hdc.DeleteDC()

    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Lade eine Schriftart
    font = ImageFont.truetype("arial.ttf", 20)
    small_font = ImageFont.truetype("arial.ttf", 16)

    # Funktion zum Zeichnen von Text
    def draw_text(text, position, font=font):
        draw.text(position, text, fill="black", font=font)

    # Zeichne die Informationen
    draw_text("Labelschnelldruck", (10, 10))
    draw_text(f"Produkt: {product_name}", (10, 40))
    if event_name:
        draw_text(f"Event: {event_name}", (10, 70))

    # Erstelle und zeichne den Barcode
    barcode_class = barcode.get_barcode_class('code128')
    barcode_image = barcode_class(barcode_data, writer=ImageWriter())
    barcode_buffer = BytesIO()
    barcode_image.write(barcode_buffer)
    barcode_image = Image.open(barcode_buffer)

    # Fixiere die Barcode-Breite und erhöhe die Höhe
    barcode_width = width - 20  # Erhöhe die Breite des Barcodes
    barcode_height = 200  # Setze die Höhe auf 200

    # Ändere die Größe des Barcodes
    resized_barcode = barcode_image.resize((barcode_width, barcode_height), Image.Resampling.BICUBIC)
    img.paste(resized_barcode, (10, 100))  # Positioniere den Barcode weiter unten

    # Position unter dem Barcode anpassen
    y_position = 100 + barcode_height + 10  # Position unter dem Barcode anpassen

    draw_text(f"Produktdatum: {product_date}", (10, y_position))
    y_position += 30
    draw_text(f"Lager: {storage_name}", (10, y_position))
    y_position += 30
    draw_text(f"Regal: {storage_shelf}", (10, y_position))
    y_position += 30
    draw_text(f"Etage: {storage_level}", (10, y_position))
    y_position += 30
    draw_text("Hinweis:", (10, y_position))
    y_position += 30
    draw_text(note, (10, y_position), small_font)
    y_position += 60
    draw_text(f"Bearbeiter: {handler}", (10, y_position))

    # Speichere das Bild
    img.save("label1.png")

    # Drucke das Bild
    print_image("label1.png")
