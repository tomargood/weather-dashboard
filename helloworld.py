import time
from weasyprint import HTML
from pdf2image import convert_from_path
from PIL import Image
from waveshare_epd.epd7in3f import EPD

# Paths
HTML_FILE = "templates/page.html"  # your Flask template
PDF_FILE = "dashboard.pdf"
PNG_FILE = "dashboard.png"
DISPLAY_TIME = 30  # seconds

def render_dashboard():
    print("Rendering dashboard to PDF...")
    HTML(HTML_FILE).write_pdf(PDF_FILE)
    print(f"Saved PDF as {PDF_FILE}")

    print("Converting PDF to PNG...")
    pages = convert_from_path(PDF_FILE, dpi=100)  # lower dpi for Pi Zero
    first_page = pages[0]
    first_page.save(PNG_FILE, "PNG")
    print(f"Saved PNG as {PNG_FILE}")

def show_on_epaper():
    print("Initializing e-paper display...")
    epd = EPD()
    epd.init()

    # Open the PNG and resize to screen
    image = Image.open(PNG_FILE)
    image = image.resize((epd.width, epd.height))
    epd.display(epd.getbuffer(image))

    print(f"Displaying for {DISPLAY_TIME} seconds...")
    time.sleep(DISPLAY_TIME)

    print("Clearing display and putting it to sleep...")
    epd.Clear()
    epd.sleep()
    print("Done.")

if __name__ == "__main__":
    render_dashboard()
    show_on_epaper()
