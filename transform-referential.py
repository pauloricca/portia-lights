#!/usr/bin/env python3

import os
import subprocess
from config import loadConfig, saveConfig
from constants import CONFIG_FILE
from utils import getAbsolutePath

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
    coords[0] = -coords[0]
    # coords[1] = coords[2] + 20
    # coords[2] = 25

saveConfig(config)

print('done.')

