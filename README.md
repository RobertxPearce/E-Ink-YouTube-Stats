# YouTube Stats Display on Waveshare E-ink Display
This repository contains the necessary code and instructions to set up a Raspberry Pi Zero W with a Waveshare Three Color 2.13-inch E-ink Display HAT to display YouTube channel statistics including subscriber count, view count, and video count. The project fetches the statistics using the YouTube Data API and updates the display at regular intervals.

## Requirements

- Raspberry Pi Zero W
- Waveshare Three Color 2.13-inch E-ink Display HAT
- MicroSD card with Raspberry Pi OS
- Wi-Fi connection
- YouTube Data API key

## Setup Instructions

### 1. Install Raspberry Pi OS

1. Download and install Raspberry Pi Imager from the [official website](https://www.raspberrypi.org/software/).
2. Use Raspberry Pi Imager to write the Raspberry Pi OS to a microSD card.
3. Create a file named `ssh` (without any extension) in the boot partition to enable SSH.
4. Create a file named `wpa_supplicant.conf` in the boot partition with your Wi-Fi credentials:
    ```plaintext
    country=US
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1

    network={
        ssid="YOUR_SSID"
        psk="YOUR_PASSWORD"
        key_mgmt=WPA-PSK
    }
    ```

### 2. Connect and Set Up the E-ink Display

1. Attach the E-ink display HAT to the GPIO pins of the Raspberry Pi Zero W.
2. Boot up the Raspberry Pi and SSH into it.
3. Update the package list and install dependencies:
    ```bash
    sudo apt update
    sudo apt upgrade -y
    sudo apt install python3-pip python3-pil python3-numpy git
    pip3 install RPi.GPIO spidev
    ```

### 3. Clone the Waveshare E-ink Repository

1. Clone the Waveshare E-ink GitHub repository:
    ```bash
    git clone https://github.com/waveshare/e-Paper
    cd e-Paper/RaspberryPi_JetsonNano/python
    sudo python3 setup.py install
    ```

### 4. Get YouTube API Key and Fetch Stats

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project and enable the YouTube Data API v3.
3. Create API credentials (API key).

### 5. Create Python Script to Display Stats

1. Install the Google API Python client:
    ```bash
    pip3 install google-api-python-client
    ```
2. Create a Python script to fetch and display YouTube stats:
    ```python
    import time
    from PIL import Image, ImageDraw, ImageFont
    from waveshare_epd import epd2in13b_V3
    from googleapiclient.discovery import build

    api_key = 'YOUR_YOUTUBE_API_KEY'
    channel_id = 'YOUR_CHANNEL_ID'

    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.channels().list(
        part='statistics',
        id=channel_id
    )
    response = request.execute()

    stats = response['items'][0]['statistics']
    subs = stats['subscriberCount']
    views = stats['viewCount']
    videos = stats['videoCount']

    epd = epd2in13b_V3.EPD()
    epd.init()

    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)

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
    ```

### 6. Run the Script

1. Save the script and run it:
    ```bash
    python3 display_youtube_stats.py
    ```

### 7. Automate the Process

1. Create a cron job to update the stats periodically:
    ```bash
    crontab -e
    ```
2. Add the following line to update the stats every hour:
    ```bash
    0 * * * * /usr/bin/python3 /home/pi/display_youtube_stats.py
    ```

## License

This project is licensed under the MIT License.

---
