#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import logging
import os
from random import randint
import re


class TimeDate():
    """ Says time and date
    """

    language  = ''
    lastQuery = ''

    text = {
            'FR': {
                'itIs': 'Il est',
                'hours': 'heures'
               }
           }

    # Load config
    def __init__(self, configFile='config.json'):
        if configFile == 'config.json':
            configFile = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(configFile, 'r') as configFile:
            # Filter comments
            config = re.sub(r'//.*\n', '\n', configFile.read())
            config = json.loads(config)
            # Parse it
            self.language = config['timeDate'].get('language', 'FR')

    def process(self, entities, currentIntent=None, lastRequest=None):
        now = datetime.datetime.now()
        speech = self.text[self.language]['itIs'] + ' '
        speech += str(now.hour) + ' '
        speech += self.text[self.language]['hours'] + ' '
        speech += str(now.minute) + '.'
        return {'keepRunning': True, 'speech': speech}
