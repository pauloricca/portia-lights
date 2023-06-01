#!/usr/bin/env python3

import os
import subprocess
from config import loadConfig, saveConfig
from constants import CONFIG_FILE
from utils import getAbsolutePath

print('(This needs to be run with sudo)')

print('Move current configuration by:')
x = float(input('x: '))
y = float(input('y: '))
z = float(input('z: '))

path = getAbsolutePath(CONFIG_FILE)

# Backup configuration
suffix = 1
backupFilePath = path + '.bk'
while os.path.isfile(backupFilePath):
    suffix += 1
    backupFilePath = path + '-' + str(suffix) + '.bk'
subprocess.call(('cp', path, backupFilePath))

config = loadConfig()

for coords in config:
    coords[0] += x
    coords[1] += y
    coords[2] += z

saveConfig(config)

print('done.')

