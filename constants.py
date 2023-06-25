import platform

# "Linux" / "Darwin" / "Windows"
PLATFORM = platform.system()

AUDIO_FILE = 'Andrey Novikov - Spider Consciousness.wav'
CONFIG_FILE = 'config.json'
HOSTS_FILE = 'hosts'
MAIN_SEQUENCE_FILE = 'main.sequence'

#LED_PIN = 18          # GPIO pin connected to the ledStrip (18 uses PWM!).
LED_PIN = 10        # GPIO pin connected to the ledStrip (10 uses SPI /dev/spidev0.0).
LED_PIN_2 = 18        # GPIO pin connected to the ledStrip (10 uses SPI /dev/spidev0.0).
LED_PIN_3 = 21        # GPIO pin connected to the ledStrip (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

TARGET_FPS = 60

# 1 means overblowing is linear, less means it takes higher values to get to full white
# Different overblow ratios per channel so we can control how it per channel.
# When all ratios are the same, the overblow tends to be bluer
OVERBLOW_BLEED_RATIO_R = 1
OVERBLOW_BLEED_RATIO_G = .5
OVERBLOW_BLEED_RATIO_B = .2

# Used to generate events in random points of space (can be different to the actual installation bounding box)
EVENTS_BOUNDING_BOX = [
    [-175, 175],
    [-65, 78],
    [-5, 30]
]

# Amount of time, in seconds, that events are send in advance to slaves
# Too short and we lose real-time event responses, too long and slaves might not have been
# online where future events were sent
SLAVE_ADVANCE_NOTICE_TIME = 2

VIRTUAL_CAMERA = (0, -20, -800)

RASPI_MAC_ADDRESS_START = 'b8'
