import time
from weasyprint import HTML
from PIL import Image
from waveshare_epd.epd7in3f import EPD

# Path to your template
HTML_FILE = "templates/dashboard.html"
PDF_FILE = "dashboard.pdf"
PNG_FILE = "dashboard.png"
DISPLAY_TIME = 30  # seconds

def render_dashboard():
    print("Rendering dashboard to PDF...")
    HTML(HTML_FILE).write_pdf(PDF_FILE)
    print(f"Saved PDF as {PDF_FILE}")

    print("Converting PDF to PNG...")
    im = Image.open(PDF_FILE)
    im = im.convert("RGB")  # ensure RGB mode
    im.save(PNG_FILE)
    print(f"Saved PNG as {PNG_FILE}")

def show_on_epaper():
    print("Initializing e-paper display...")
    epd = EPD()
    epd.init()

    # Open PNG and resize to screen
    image = Image.open(PNG_FILE)
    image = image.resize((epd.width, epd.height))
    epd.display(epd.getbuffer(image))

    print(f"Displaying for {DISPLAY_TIME} seconds...")
    time.sleep(DISPLAY_TIME)

    print("Clearing display and sleeping...")
    epd.Clear()
    epd.sleep()
    print("Done.")

if __name__ == "__main__":
    render_dashboard()
    show_on_epaper()
