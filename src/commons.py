import importlib.metadata
import logging
from enum import auto

import json

from dynaconf import Dynaconf

settings = Dynaconf(settings_files=["conf/settings.toml", "conf/.secrets.toml"],
                    environments=True)

logging.basicConfig(filename=settings.LOG_FILE, level=settings.LOG_LEVEL,
                    format=settings.LOG_FORMAT)

__version__ = importlib.metadata.metadata("dans-file-format-service")["version"]

data = {}

all_formats = {"M4A", "AAC", "WAV", "AIFF", "MP3", "BWF", "MKA", "FLAC", "OPUS", "MXF", "AVI", "M4V", "MP4", "MOV", "MPG", "MPEG", "M2V", "MPG2", "QT", "MXF", "MKV"}