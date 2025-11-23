#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
from PIL import Image, ImageDraw, ImageFont

# Import Waveshare e-paper driver
from waveshare_epd import epd7in3f

def main():
    try:
        # Initialize display
        epd = epd7in3f.EPD()
        epd.init()
        epd.Clear()

        # Load font (make sure Font.ttc exists in your project folder)
        font_path = "Font.ttc"  # Adjust if stored elsewhere
        font = ImageFont.truetype(font_path, 48)

        # Create blank canvas
        img = Image.new('RGB', (epd.width, epd.height), epd.WHITE)
        draw = ImageDraw.Draw(img)

        # Rainbow colors supported by the display
        rainbow = [epd.RED, epd.ORANGE, epd.YELLOW, epd.GREEN, epd.BLUE, epd.BLACK]

        y = 40
        for color in rainbow:
            draw.text((20, y), "HELLO WORLD", font=font, fill=color)
            y += 60

        # Display the image
        epd.display(epd.getbuffer(img))

        # Hold for 10 seconds
        time.sleep(10)

        # Clear and sleep
        epd.Clear()
        epd.sleep()
        print("Done!")

    except KeyboardInterrupt:
        print("Ctrl+C detected, exiting...")
        epd7in3f.epdconfig.module_exit(cleanup=True)
    except Exception as e:
        print("Error:", e)
        epd7in3f.epdconfig.module_exit(cleanup=True)

if __name__ == "__main__":
    main()