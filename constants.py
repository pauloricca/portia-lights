#import board

AUDIO_FILE = "temple.wav"
CONFIG_FILE = "config.json"

LED_COUNT = 18
#LED_PIN = board.D10 # 10 uses SPI /dev/spidev0.0 (pin 19)
#LED_PIN = board.D18 # PWM (pin 12) - needs to be run with sudo

#LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

SLEEP_TIME_PER_FRAME = 0.01

# 1 means overblowing is linear, less means it takes higher values to get to full white
# Different overblow ratios per channel so we can control how it per channel.
# When all ratios are the same, the overblow tends to be bluer
OVERBLOW_BLEED_RATIO_R = 1
OVERBLOW_BLEED_RATIO_G = .5
OVERBLOW_BLEED_RATIO_B = .2

SPACE_BOUNDING_BOX = [
    [0, 5],
    [-2, 10],
    [0, 0]
]