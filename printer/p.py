import win32print
import win32ui
from PIL import Image, ImageWin


def print_image(file_path):
    printer_name = win32print.GetDefaultPrinter()

    # Create DC
    hdc = win32ui.CreateDC()
    hdc.CreatePrinterDC(printer_name)

    # Get printer capabilities
    printer_width = hdc.GetDeviceCaps(110)  # PHYSICALWIDTH
    printer_height = hdc.GetDeviceCaps(111)  # PHYSICALHEIGHT

    # Load and resize image to match printer dimensions
    bmp = Image.open(file_path)
    bmp = bmp.resize((printer_width, printer_height), Image.LANCZOS)

    # Start doc
    hdc.StartDoc("Label Print")
    hdc.StartPage()

    # Draw image
    dib = ImageWin.Dib(bmp)
    dib.draw(hdc.GetHandleOutput(), (0, 0, printer_width, printer_height))

    # End
    hdc.EndPage()
    hdc.EndDoc()
    hdc.DeleteDC()


if __name__ == "__main__":
    print_image("test_image.png")