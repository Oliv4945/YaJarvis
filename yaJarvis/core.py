#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import log
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import importlib
import json
import logging
import requests
import pprint
from plugins import *


class PluginsList():
    pluginsList = {
            'weather': weatherWunderground.WeatherWunderground
          }

    def __init__(self):
        for key, module in self.pluginsList.items():
            setattr(self, key, module())


class RasaRequest():
    entities = {}
    intent = {}
    keepRunning = False


# HTTPRequestHandler class
class MyHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        queryText = parse_qs(self.path[2:]).get('query', [None])[0]

        # If wrong query
        if queryText is None:
            self.send_response(418)
            return

        # Send headers
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=UTF-8')
        self.end_headers()

        """
        # If only one or two  words, pass it to last intent
        if queryText.count(' ') < 2:
            message = (getattr(self.pluginsList, self.lastRequest['intent']['name'])
                       .process({'noRasa':queryText}, self.lastRequest)
                       )
            self.wfile.write(message['speech'].encode('utf8'))
            return
        """

        # Query Rasa NLU and parse results
        data = json.dumps({'q': queryText})
        try:
            r = requests.post('http://localhost:10000/parse', data)
        except requests.exceptions.ConnectionError:
            self.wfile.write('Connection error to Rasa server'.encode('utf8'))
            return

        pp = pprint.PrettyPrinter(indent=4)
        print('CORE - Rasa JSON')
        pp.pprint(r.json())
        intent = r.json()['intent']
        entities = {}
        for entity in r.json()['entities']:
            entities[entity['entity']] = entity['value']
        logging.info('CORE -- intent: %s', intent)
        logging.info('CORE -- entities: %s', entities)

        # Call last intent if 'all' is detected
        if intent['name'] == 'all':
            message = (getattr(self.pluginsList, self.lastRequest['intent']['name'])
                       .process(entities, self.lastRequest)
                       )
            self.wfile.write(message['speech'].encode('utf8'))
            return
        message = (getattr(self.pluginsList, intent['name'])
                    .process(entities, self.lastRequest)
                   )
        self.wfile.write(message['speech'].encode('utf8'))

        # Save context
        self.lastRequest['intent']      = intent
        self.lastRequest['entities']    = entities
        self.lastRequest['keepRunning'] = message.get('keepRunning', False)
        return


def run():
    # Server settings
    server_address = ('0.0.0.0', 10001)
    httpd = HTTPServer(server_address, MyHandler)
    MyHandler.pluginsList = PluginsList()
    MyHandler.lastRequest = {}
    try:
        logging.info('CORE - Running Jarvis backend')
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    run()
