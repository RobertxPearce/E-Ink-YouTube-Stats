import time
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13b_V3
from googleapiclient.discovery import build

# Configuration
api_key = 'YOUR_YOUTUBE_API_KEY'  # ***Replace with your YouTube Data API key***
channel_id = 'YOUR_CHANNEL_ID'    # ***Replace with your YouTube channel ID***

# Initialize YouTube API
youtube = build('youtube', 'v3', developerKey=api_key)

def fetch_youtube_stats():
    request = youtube.channels().list(
        part='statistics',
        id=channel_id
    )
    response = request.execute()

    stats = response['items'][0]['statistics']
    return stats['subscriberCount'], stats['viewCount'], stats['videoCount']

def display_stats(subs, views, videos):
    epd = epd2in13b_V3.EPD()
    epd.init()
    
    # Create a blank image
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)
    
    # Load a font
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)

    # Draw lines and text
    draw.line((0, 0, epd.width, 0), fill=0)
    draw.line((0, epd.height-1, epd.width, epd.height-1), fill=0)
    draw.text((10, 10), 'Subscribers:', font=font, fill=0)
    draw.text((10, 40), 'Views:', font=font, fill=0)
    draw.text((10, 70), 'Videos:', font=font, fill=0)
    draw.text((140, 10), subs, font=font, fill=0)
    draw.text((140, 40), views, font=font, fill=0)
    draw.text((140, 70), videos, font=font, fill=0)

    # Draw YouTube logo
    youtube_logo = Image.open('path_to_youtube_logo.png')  # Ensure you have a logo file
    image.paste(youtube_logo, (epd.width - youtube_logo.width - 10, 10))

    epd.display(epd.getbuffer(image))
    epd.sleep()

if __name__ == '__main__':
    while True:
        subs, views, videos = fetch_youtube_stats()
        display_stats(subs, views, videos)
        time.sleep(3600)  # Update every hour
