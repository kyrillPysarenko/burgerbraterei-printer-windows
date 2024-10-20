import win32print
import win32ui

# Setze den Standarddrucker
printer_name = win32print.GetDefaultPrinter()
print(f"Verwendeter Drucker: {printer_name}")

# Öffne den Drucker
h_printer = win32print.OpenPrinter(printer_name)

# Abrufen der Druckereinstellungen (DevMode)
printer_info = win32print.GetPrinter(h_printer, 2)
devmode = printer_info['pDevMode']

# Setze die Papierbreite und -länge explizit (in Zehntelmillimeter)
devmode.PaperWidth = int(62 * 10)  # 62 mm Breite
devmode.PaperLength = int(90 * 10)  # Beispiel: 90 mm Länge

# Setze die Druckereinstellungen zurück in den Drucker
win32print.SetPrinter(h_printer, 2, printer_info, 0)

# Erstelle das Device Context (DC) für den Drucker
hDC = win32ui.CreateDC()
hDC.CreatePrinterDC(printer_name)
hDC.SetMapMode(6)  # Setze Modus auf MM_TWIPS

# Starte den Druckauftrag
try:
    # Initialisiere das Dokument
    win32print.StartDocPrinter(h_printer, 1, ("Testdruck", None, "RAW"))
    win32print.StartPagePrinter(h_printer)

    # Drucktext
    hDC.SetTextColor(0x000000)  # Textfarbe Schwarz
    hDC.TextOut(100, 100, "Testdruck auf 62 mm Etikett")  # Textausgabe an definierter Position

    # Schließe den Druckauftrag
    win32print.EndPagePrinter(h_printer)
    win32print.EndDocPrinter(h_printer)

    print("Druckauftrag abgeschlossen.")

except Exception as e:
    print(f"Fehler beim Druckvorgang: {e}")

finally:
    # Schließe den Drucker
    win32print.ClosePrinter(h_printer)
    hDC.DeleteDC()
