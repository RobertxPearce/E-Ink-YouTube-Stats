#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
import time
import requests
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13_V3
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Your YouTube API key
API_KEY = 'AIzaSyC4RfxUyo7S0f_pflCMOU1ThgSMVjofoK8'

# Your YouTube channel ID
CHANNEL_ID = 'UC8tHiyp4m4q2o3FtZWK54tQ'  # Replace this with your actual channel ID

def get_youtube_stats(api_key, channel_id):
    """
    Fetch YouTube channel statistics using YouTube Data API.

    Parameters:
        api_key (str): Your YouTube Data API key.
        channel_id (str): Your YouTube channel ID.

    Returns:
        dict: A dictionary containing channel statistics.
    """
    url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}'
    response = requests.get(url)  # Make the API request
    data = response.json()  # Parse the JSON response

    # Debugging: print the response data
    print(data)

    # Check if 'items' key is in the response data
    if 'items' not in data or len(data['items']) == 0:
        raise ValueError("Invalid response received from YouTube API or incorrect channel ID.")

    # Extract statistics
    stats = data['items'][0]['statistics']
    return stats

def display_stats_on_eink(stats):
    """
    Display YouTube channel statistics on the e-ink display.

    Parameters:
        stats (dict): A dictionary containing channel statistics.
    """
    try:
        logging.info("Initializing e-ink display...")  # Log the initialization
        epd = epd2in13_V3.EPD()  # Initialize the e-ink display object
        logging.info("init and Clear")  # Log the initialization and clearing
        epd.init()  # Initialize the e-ink display
        epd.Clear(0xFF)  # Clear the display

        # Create an image with PIL for black content
        black_image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw_black = ImageDraw.Draw(black_image)  # Create a drawing context

        # Use a truetype font
        font = ImageFont.truetype('/home/pi/youtube_stats_display/fonts/DejaVuSans-Bold.ttf', 18)

        # Display the stats
        draw_black.text((10, 10), 'Subscribers:', font=font, fill=0)  # Draw subscriber label
        draw_black.text((150, 10), f'{stats["subscriberCount"]}', font=font, fill=0)  # Draw subscriber count
        draw_black.text((10, 40), 'Views:', font=font, fill=0)  # Draw views label
        draw_black.text((150, 40), f'{stats["viewCount"]}', font=font, fill=0)  # Draw views count
        draw_black.text((10, 70), 'Videos:', font=font, fill=0)  # Draw videos label
        draw_black.text((150, 70), f'{stats["videoCount"]}', font=font, fill=0)  # Draw videos count

        # Display the image on the e-ink display
        epd.display(epd.getbuffer(black_image))
        logging.info("Stats displayed on e-ink.")  # Log the display update

    except IOError as e:
        logging.info(e)  # Log IO errors
    except KeyboardInterrupt:
        logging.info("ctrl + c:")  # Log the keyboard interrupt
        epd2in13_V3.epdconfig.module_exit(cleanup=True)  # Clean up GPIO
        exit()  # Exit the script

if __name__ == '__main__':
    try:
        while True:
            stats = get_youtube_stats(API_KEY, CHANNEL_ID)  # Fetch YouTube stats
            display_stats_on_eink(stats)  # Display the stats on the e-ink display
            # Wait for 5 minutes before updating again
            time.sleep(300)  # Sleep for 300 seconds (5 minutes)
    except Exception as e:
        print(f"Error: {e}")  # Print any exceptions that occur
    except KeyboardInterrupt:
        logging.info("ctrl + c:")  # Log the keyboard interrupt
        epd2in13_V3.epdconfig.module_exit(cleanup=True)  # Clean up GPIO
        exit()  # Exit the script
