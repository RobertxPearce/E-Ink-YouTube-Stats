# YouTube Stats Display on Waveshare E-ink Display

This project sets up a Raspberry Pi Zero W with a Waveshare Three Color 2.13-inch E-ink Display HAT to display YouTube channel statistics, including subscriber count, view count, and video count. The stats are fetched using the YouTube Data API and displayed in a organized layout.

### Closer Look
![IMG_2956](https://github.com/user-attachments/assets/a0a40e8c-6dfb-4857-937e-7bb5dd4433d1)


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
    sudo apt install python3-RPi.GPIO python3-spidev
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
2. Use the provided `display_youtube_stats.py` script in this repository to fetch and display YouTube stats. Make sure to update the script with your YouTube API key and channel ID.

### 6. Run the Script

1. Run the script once (wont update after session is closed):
    ```bash
    python3 display_youtube_stats.py
    ```
2. Run the script in the background:
    ```bash
    nohup python3 your_script_name.py &
    ```

## License

This project is licensed under the MIT License.

