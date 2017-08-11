#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.config
from logging.handlers import RotatingFileHandler

LEVEL = logging.INFO
FILE  = 'log_YaJarvis.log'

logger = logging.getLogger()
logger.setLevel(LEVEL)

formatter = logging.Formatter('%(asctime)s -- %(levelname)s -- %(message)s')

# Log to a file
file_handler = RotatingFileHandler(FILE, 'a', 1000000, 1)
file_handler.setLevel(LEVEL)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Log to console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
