#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
from PIL import Image, ImageDraw, ImageFont

# Import the Waveshare driver from the same folder
from epd7in3f import EPD

def main():
    try:
        # Initialize display
        epd = EPD()
        epd.init()
        epd.Clear()

        # Load font (adjust if you have a different path or font)
        font = ImageFont.truetype("Font.ttc", 48)

        # Create blank canvas
        img = Image.new('RGB', (epd.width, epd.height), epd.WHITE)
        draw = ImageDraw.Draw(img)

        # Rainbow colors supported by the panel
        rainbow = [epd.RED, epd.ORANGE, epd.YELLOW, epd.GREEN, epd.BLUE, epd.BLACK]

        y = 40
        for color in rainbow:
            draw.text((20, y), "HELLO WORLD", font=font, fill=color)
            y += 60

        # Display the image
        epd.display(epd.getbuffer(img))

        # Keep displayed for 10 seconds
        time.sleep(10)

        # Clear and put the display to sleep
        epd.Clear()
        epd.sleep()
        print("Done!")

    except KeyboardInterrupt:
        print("Ctrl+C detected, exiting...")
        epd7in3f.EPD.module_exit()  # cleanup if user interrupts
    except Exception as e:
        print("Error:", e)
        epd7in3f.EPD.module_exit()

if __name__ == "__main__":
    main()
