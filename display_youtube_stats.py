import time
import requests
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13_V3
import logging

# Configure logging to display debug messages.
logging.basicConfig(level=logging.DEBUG)

# YouTube API key and channel ID.
API_KEY = 'YOUR API KEY'
CHANNEL_ID = 'YOUR CHANNEL ID'


def get_youtube_stats(api_key, channel_id):
    """
    Fetch YouTube channel statistics using the YouTube Data API.

    Parameters:
        api_key (str): Your YouTube Data API key.
        channel_id (str): Your YouTube channel ID.

    Returns:
        dict: A dictionary containing channel statistics.
    """
    # Construct the API request URL.
    url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}'
    
    # Make the API request.
    response = requests.get(url)
    
    # Parse the JSON response.
    data = response.json()
    
    # Check if 'items' key is in the response data.
    if 'items' not in data or len(data['items']) == 0:
        raise ValueError("Invalid response received from YouTube API or incorrect channel ID.")
    
    # Extract and return the statistics.
    return data['items'][0]['statistics']


def display_stats_on_eink(stats):
    """
    Display YouTube channel statistics on the e-ink display.

    Parameters:
        stats (dict): A dictionary containing channel statistics.
    """
    try:
        # Initialize the e-ink display.
        epd = epd2in13_V3.EPD()
        epd.init()
        epd.Clear(0xFF)

        # Create a blank image for the black content.
        black_image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw_black = ImageDraw.Draw(black_image)

        # Load a TrueType font.
        font = ImageFont.truetype('/home/pi/youtube_stats_display/fonts/DejaVuSans-Bold.ttf', 18)

        # Draw the statistics on the image.
        draw_black.text((10, 10), 'Subscribers:', font=font, fill=0)
        draw_black.text((150, 10), f'{stats["subscriberCount"]}', font=font, fill=0)
        draw_black.text((10, 40), 'Views:', font=font, fill=0)
        draw_black.text((150, 40), f'{stats["viewCount"]}', font=font, fill=0)
        draw_black.text((10, 70), 'Videos:', font=font, fill=0)
        draw_black.text((150, 70), f'{stats["videoCount"]}', font=font, fill=0)

        # Display the image on the e-ink display.
        epd.display(epd.getbuffer(black_image))

    except Exception as e:
        # Log any errors and clean up the GPIO.
        logging.error(f"Error: {e}")
        epd2in13_V3.epdconfig.module_exit(cleanup=True)


if __name__ == '__main__':
    try:
        while True:
            try:
                # Fetch YouTube statistics.
                stats = get_youtube_stats(API_KEY, CHANNEL_ID)
                
                # Display the statistics on the e-ink display.
                display_stats_on_eink(stats)
                
            except Exception as e:
                # Log any errors during the update process.
                logging.error(f"Error during update: {e}")
            
            # Wait for 5 minutes before updating again.
            time.sleep(300)
    
    except KeyboardInterrupt:
        # Log the interruption and clean up the GPIO.
        logging.info("Program interrupted")
        epd2in13_V3.epdconfig.module_exit(cleanup=True)
