
#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import time
import logging
from PIL import Image, ImageDraw, ImageFont

# Setup Waveshare library paths
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd7in3f

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("7.3in e-Paper Simple Hello World")

    epd = epd7in3f.EPD()
    epd.init()
    epd.Clear()

    # Choose a nice readable font
    font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 48)

    # Create a blank canvas
    Himage = Image.new('RGB', (epd.width, epd.height), epd.WHITE)
    draw = ImageDraw.Draw(Himage)

    # Rainbow color list (panel supports BLACK/WHITE/RED/YELLOW/ORANGE/GREEN/BLUE)
    rainbow_colors = [
        epd.RED,
        epd.ORANGE,
        epd.YELLOW,
        epd.GREEN,
        epd.BLUE,
        epd.BLACK
    ]

    # Draw "Hello World" 6 times in rainbow colors
    y = 40
    for color in rainbow_colors:
        draw.text((20, y), "HELLO WORLD", font=font, fill=color)
        y += 60

    # Display it
    epd.display(epd.getbuffer(Himage))

    # Hold for 10 seconds
    time.sleep(10)

    # Clear and sleep
    epd.Clear()
    epd.sleep()

except Exception as e:
    logging.error(e)
    epd7in3f.epdconfig.module_exit(cleanup=True)
