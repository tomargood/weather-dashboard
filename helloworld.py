import time
from PIL import Image, ImageDraw, ImageFont

# Correct import from the local waveshare_epd folder
from waveshare_epd.epd7in3f import EPD

def main():
    # Initialize the display
    epd = EPD()
    epd.init()  # some versions use epd.Init() instead of epd.init()
    
    # Create a blank image (white background)
    image = Image.new('RGB', (epd.width, epd.height), epd.WHITE)
    draw = ImageDraw.Draw(image)

    # Load a font if available, fallback to default
    try:
        font = ImageFont.truetype("Font.ttc", 48)
    except:
        font = ImageFont.load_default()

    # Draw Hello World
    draw.text((20, 20), "HELLO WORLD", fill=epd.BLACK, font=font)

    # Display the image
    epd.display(epd.getbuffer(image))

    # Hold the display for 10 seconds
    time.sleep(10)

    # Clear and put the display to sleep
    epd.clear()
    epd.sleep()

    print("Finished displaying Hello World!")

if __name__ == "__main__":
    main()