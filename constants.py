import board

AUDIO_FILE = "temple.wav"

LED_COUNT = 200
#LED_PIN = board.D10 # 10 uses SPI /dev/spidev0.0 (pin 19)
LED_PIN = board.D18 # PWM (pin 12) - needs to be run with sudo

# 1 means overblowing is linear, less means it takes higher values to get to full white
# Different overblow ratios per channel so we can control how it per channel.
# When all ratios are the same, the overblow tends to be bluer
OVERBLOW_BLEED_RATIO_R = 1
OVERBLOW_BLEED_RATIO_G = .5
OVERBLOW_BLEED_RATIO_B = .2