import win32print
import win32ui
from PIL import Image, ImageWin

def print_image(file_path):
    printer_name = win32print.GetDefaultPrinter()

    # Erstelle DC
    hdc = win32ui.CreateDC()
    hdc.CreatePrinterDC(printer_name)

    # Hole die Druckerfähigkeiten
    printer_width = hdc.GetDeviceCaps(110)  # PHYSICALWIDTH
    printer_height = hdc.GetDeviceCaps(111)  # PHYSICALHEIGHT

    # Lade und skaliere das Bild auf die Druckergröße
    bmp = Image.open(file_path)
    bmp = bmp.resize((printer_width, printer_height), Image.LANCZOS)

    # Starte das Dokument
    hdc.StartDoc("Label Print")
    hdc.StartPage()

    # Zeichne das Bild
    dib = ImageWin.Dib(bmp)
    dib.draw(hdc.GetHandleOutput(), (0, 0, printer_width, printer_height))

    # Beende
    hdc.EndPage()
    hdc.EndDoc()
    hdc.DeleteDC()
