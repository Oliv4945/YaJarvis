#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import os
from random import randint
import re
import requests
import string


class WeatherWunderground():
    """ Get weather forecast from Wunderground
    """

    apiKey    = ''
    country   = None
    language  = ''
    waitState = ''
    lastQuery = ''

    text = {
            'FR': {
                'cityHomonyms'  : [
                    'Plusieurs /CITY/ trouvées, est-ce en ',
                    'Plusieurs villes correspondent, quel département ?',
                   ],
                'cityNotFound'  : [
                    "/CITY/ n'est pas disponible.",
                    'Je ne trouve pas la ville de /CITY/.',
                    'Pas de station météo à /CITY/.'
                   ],
                'decimalSeparator'  : 'virgule',
                'degrees': 'degrés',
                'error'  : ['Erreur du serveur météo.'],
                'locationRequired': 'Dans quelle ville ?',
                'keyError':['Mauvaise clef API Wunderground.'],
                'kph'    : 'kilomètre heure',
                'noWind' : 'pas de vent',
                'repeatState': ['Je ne trouve pas, quel département ?'],
                'wind'   : 'vent',
                'windDir': {
                        'north'    : 'de Nord',
                        'south'    : 'de Sud',
                        'east'     : "d'Est",
                        'west'     : "d'Ouest",
                        'northEast': 'de Nord Est',
                        'northWest': 'de Nord Ouest',
                        'southEast': 'de Sud Est',
                        'southWest': 'de Sud Ouest'
                   }
               }
           }
    windDirDict = {
            'NNO': 'north', 'NNW'  : 'north', 'North': 'north', 'NNE': 'north',
            'SSE': 'south', 'SSW'  : 'south', 'South': 'south', 'SSO': 'south',
            'ESE': 'east',  'East' : 'east',  'ENE'  : 'east',
            'OSO': 'west',  'West' : 'west',  'ONO'  : 'west',
            'WNW': 'west', 'WSW': 'west',
            'NE' : 'northEast',
            'NO' : 'northWest', 'NW': 'northWest',
            'SE' : 'southEast',
            'SO' : 'southWest', 'SW': 'southWest'
       }

    statesDict = {
            'FR': {
                # From: https://gist.github.com/mlorant/b4d7bb6f96c47776c8082cf7af44ad95
                '01': 'Ain',
                '02': 'Aisne',
                '03': 'Allier',
                '04': 'Alpes-de-Haute-Provence',
                '05': 'Hautes-Alpes',
                '06': 'Alpes-Maritimes',
                '07': 'Ardèche',
                '08': 'Ardennes',
                '09': 'Ariège',
                '10': 'Aube',
                '11': 'Aude',
                '12': 'Aveyron',
                '13': 'Bouches-du-Rhône',
                '14': 'Calvados',
                '15': 'Cantal',
                '16': 'Charente',
                '17': 'Charente-Maritime',
                '18': 'Cher',
                '19': 'Corrèze',
                '2A': 'Corse-du-Sud',
                '2B': 'Haute-Corse',
                '21': 'Côte-d\'Or',
                '22': 'Côtes-d\'Armor',
                '23': 'Creuse',
                '24': 'Dordogne',
                '25': 'Doubs',
                '26': 'Drôme',
                '27': 'Eure',
                '28': 'Eure-et-Loir',
                '29': 'Finistère',
                '30': 'Gard',
                '31': 'Haute-Garonne',
                '32': 'Gers',
                '33': 'Gironde',
                '34': 'Hérault',
                '35': 'Ille-et-Vilaine',
                '36': 'Indre',
                '37': 'Indre-et-Loire',
                '38': 'Isère',
                '39': 'Jura',
                '40': 'Landes',
                '41': 'Loir-et-Cher',
                '42': 'Loire',
                '43': 'Haute-Loire',
                '44': 'Loire-Atlantique',
                '45': 'Loiret',
                '46': 'Lot',
                '47': 'Lot-et-Garonne',
                '48': 'Lozère',
                '49': 'Maine-et-Loire',
                '50': 'Manche',
                '51': 'Marne',
                '52': 'Haute-Marne',
                '53': 'Mayenne',
                '54': 'Meurthe-et-Moselle',
                '55': 'Meuse',
                '56': 'Morbihan',
                '57': 'Moselle',
                '58': 'Nièvre',
                '59': 'Nord',
                '60': 'Oise',
                '61': 'Orne',
                '62': 'Pas-de-Calais',
                '63': 'Puy-de-Dôme',
                '64': 'Pyrénées-Atlantiques',
                '65': 'Hautes-Pyrénées',
                '66': 'Pyrénées-Orientales',
                '67': 'Bas-Rhin',
                '68': 'Haut-Rhin',
                '69': 'Rhône',
                '70': 'Haute-Saône',
                '71': 'Saône-et-Loire',
                '72': 'Sarthe',
                '73': 'Savoie',
                '74': 'Haute-Savoie',
                '75': 'Paris',
                '76': 'Seine-Maritime',
                '77': 'Seine-et-Marne',
                '78': 'Yvelines',
                '79': 'Deux-Sèvres',
                '80': 'Somme',
                '81': 'Tarn',
                '82': 'Tarn-et-Garonne',
                '83': 'Var',
                '84': 'Vaucluse',
                '85': 'Vendée',
                '86': 'Vienne',
                '87': 'Haute-Vienne',
                '88': 'Vosges',
                '89': 'Yonne',
                '90': 'Territoire de Belfort',
                '91': 'Essonne',
                '92': 'Hauts-de-Seine',
                '93': 'Seine-Saint-Denis',
                '94': 'Val-de-Marne',
                '95': 'Val-d\'Oise',
                '971': 'Guadeloupe',
                '972': 'Martinique',
                '973': 'Guyane',
                '974': 'La Réunion',
                '976': 'Mayotte',
           }
       }

    def __init__(self, configFile='config.json'):
        # Load config
        if configFile == 'config.json':
            configFile = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(configFile, 'r') as configFile:
            # Filter comments
            config = re.sub(r'//.*\n', '\n', configFile.read())
            config = json.loads(config)
            # Parse it
            self.apiKey   = config['weatherWunderground'].get('apiKey', '')
            self.language = config['weatherWunderground'].get('language', 'FR')
            self.country  = config['weatherWunderground'].get('country', None)

    def getWeatherBycity(self, city):
        # Prepare query
        url = 'http://api.wunderground.com/api/'
        url += self.apiKey
        url += '/conditions/lang:'
        url += self.language
        url += '/q/'
        if self.country is not None:
            url += self.country + '/'
        url += city
        url += '.json'
        return url

    def getWeatherFromState(self, state):
        stateNumber = None
        endpoint    = None
        # Get city endpoint
        statesDictReverse = {}
        regex = re.compile('[^%s]' % string.ascii_letters)
        for k, v in self.statesDict[self.language].items():
            v = regex.sub('', v)
            statesDictReverse[v] = k
        try:
            state = regex.sub('', state)
            stateNumber = statesDictReverse[state]
            #break
        except KeyError:
            pass
        if stateNumber is None:
            return None
        for cityData in self.lastQuery['response']['results']:
            if cityData['state'] == stateNumber:
                endpoint = cityData['l']
                break
        if endpoint is None:
            return None

        # Prepare query
        url = 'http://api.wunderground.com/api/'
        url += self.apiKey
        url += '/conditions/lang:'
        url += self.language
        url += endpoint
        url += '.json'
        return url

    def parseWeather(self, data):
        # Extract data
        temp_c   = data['current_observation']['temp_c']
        wind_kph = data['current_observation']['wind_kph']
        wind_dir = data['current_observation']['wind_dir']

        # Parse wind
        try:
            wind_dir = self.windDirDict[wind_dir]
            wind_dir = self.text[self.language]['windDir'][wind_dir]
        except KeyError:
            wind_dir = data['current_observation']['wind_dir']

        # Build answer
        speech = data['current_observation']['weather'] + ', '
        speech += str(temp_c) + ' '
        speech += self.text[self.language]['degrees'] + ', '
        if (wind_kph > 0):
            speech += self.text[self.language]['wind'] + ' ' + wind_dir + ', '
            speech += str(wind_kph) + ' '
            speech += self.text[self.language]['kph']
        else:
            speech += self.text[self.language]['noWind']
        speech.replace(
                '.', ' %s ' % self.text[self.language]['decimalSeparator']
                )
        speech += '.'
        logging.info('WEATHER -- speech: %s', speech)
        self.waitState = 'weather'
        return {'keepRunning': True, 'speech': speech}

    def process(self, entities, currentIntent=None, lastRequest=None):
        if currentIntent == 'all' and self.waitState == 'homonyms':
            url = self.getWeatherFromState(entities['state'])
            if url is None:
                return {
                        'keepRunning': True,
                        'speech': self.text[self.language]['repeatState'][0]
                        }

        elif entities.get('location', None) is None:
            return {
                    'keepRunning': True,
                    'speech': self.text[self.language]['locationRequired']
                    }
        else:
            url = self.getWeatherBycity(entities.get('location'))
        logging.info('WEATHER -- url: %s', url)

        # Call Wunderground server
        r = requests.get(url)
        logging.debug('WEATHER -- Wunderground JSON: %s', r.json())

        # Check for errors
        if 'error' in r.json()['response']:
            # City not found
            if r.json()['response']['error'].get('type', None) == 'querynotfound':
                speech = (self.text[self.language]['cityNotFound'][randint(0, 2)]
                              .replace('/CITY/', entities.get('location'))
                          )
                return {'speech': speech}
            # Wrong API key
            elif r.json()['response']['error'].get('type', None) == 'keynotfound':
                speech = (self.text[self.language]['keyError'][0]
                          )
                return {'speech': speech}
            else:
                return {'speech': self.text[self.language]['error'][0]}

        self.lastQuery = r.json()

        # Check if homonyms are found
        if 'results' in r.json()['response']:
            speech = (self.text[self.language]['cityHomonyms'][randint(0, 1)]
                          .replace('/CITY/', entities.get('location'))
                      )
            speech += ' '
            for city in r.json()['response']['results']:
                speech += self.statesDict[self.language][city['state']] + ', '
            self.waitState = 'homonyms'
            return {'keepRunning': True, 'speech': speech}

        # Code refactoring
        return self.parseWeather(r.json())
