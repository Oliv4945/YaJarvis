#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import requests_mock
from . import weatherWunderground


@pytest.fixture()
def dut():
    """ Fixture for test initialisation
    """
    return weatherWunderground.WeatherWunderground()


def testNoCity(dut):
    res = dut.process({})
    assert res['speech'] == 'Dans quelle ville ?' 
    assert res.get('keepRunning', False) is True

def testCityHomonyms(dut):
    city = 'Fontaine'
    json = {"response":{"results":[{"name":"Fontaine","city":"Fontaine","state":"03","country":"FR","country_iso3166":"FR","country_name":"France","zmw":"00000.24.07374","l":"/q/zmw:00000.24.07374"},{"name":"Fontaine","city":"Fontaine","state":"10","country":"FR","country_iso3166":"FR","country_name":"France","zmw":"00000.331.07276","l":"/q/zmw:00000.331.07276"},{"name":"Fontaine","city":"Fontaine","state":"21","country":"FR","country_iso3166":"FR","country_name":"France","zmw":"00000.363.07270","l":"/q/zmw:00000.363.07270"}]}}
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, json=json) 
        res = dut.process({'location': city, 'weatherType': 'meteo'})
        speech = res['speech']
        assert 'Allier' in speech
        assert 'Aube' in speech
        assert "Côte-d'Or" in speech
        assert speech.replace(city, '/CITY/')[:35] in [text[:35] for text in dut.text['FR']['cityHomonyms']]
        assert res.get('keepRunning', False) is True

def testCity(dut):
    json = {"response":{"version":"0.1","termsofService":"http://www.wunderground.com/weather/api/d/terms.html","features":{"conditions":1}},"current_observation":{"image":{"url":"http://icons.wxug.com/graphics/wu2/logo_130x80.png","title":"Weather Underground","link":"http://www.wunderground.com"},"display_location":{"full":"Grenoble, France","city":"Grenoble","state":"38","state_name":"France","country":"FR","country_iso3166":"FR","zip":"00000","magic":"254","wmo":"07487","latitude":"45.18999863","longitude":"5.73000002","elevation":"210.9"},"observation_location":{"full":"Grenoble, ","city":"Grenoble","state":"","country":"FR","country_iso3166":"FR","latitude":"45.36999893","longitude":"5.32999992","elevation":"1266 ft"},"estimated":{},"station_id":"LFLS","observation_time":"Last Updated on août 10, 17:30 CEST","observation_time_rfc822":"Thu, 10 Aug 2017 17:30:00 +0200","observation_epoch":"1502379000","local_time_rfc822":"Thu, 10 Aug 2017 17:49:03 +0200","local_epoch":"1502380143","local_tz_short":"CEST","local_tz_long":"Europe/Paris","local_tz_offset":"+0200","weather":"Partiellement nuageux","temperature_string":"68 F (20 C)","temp_f":68,"temp_c":20,"relative_humidity":"37%","wind_string":"From the ENE at 4 MPH","wind_dir":"ENE","wind_degrees":70,"wind_mph":4,"wind_gust_mph":0,"wind_kph":6,"wind_gust_kph":0,"pressure_mb":"1018","pressure_in":"30.06","pressure_trend":"0","dewpoint_string":"41 F (5 C)","dewpoint_f":41,"dewpoint_c":5,"heat_index_string":"NA","heat_index_f":"NA","heat_index_c":"NA","windchill_string":"NA","windchill_f":"NA","windchill_c":"NA","feelslike_string":"68 F (20 C)","feelslike_f":"68","feelslike_c":"20","visibility_mi":"6.2","visibility_km":"10.0","solarradiation":"--","UV":"2","precip_1hr_string":"-9999.00 in (-9999.00 mm)","precip_1hr_in":"-9999.00","precip_1hr_metric":"--","precip_today_string":"0.00 in (0.0 mm)","precip_today_in":"0.00","precip_today_metric":"0.0","icon":"partlycloudy","icon_url":"http://icons.wxug.com/i/c/k/partlycloudy.gif","forecast_url":"http://www.wunderground.com/global/stations/07487.html","history_url":"http://www.wunderground.com/history/airport/LFLS/2017/8/10/DailyHistory.html","ob_url":"http://www.wunderground.com/cgi-bin/findweather/getForecast?query=45.36999893,5.32999992","nowcast":""}}
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, json=json)
        res = dut.process({'location': 'Grenoble', 'weatherType': 'meteo'})
        assert res['speech'] == "Partiellement nuageux, 20 degrés, vent d'Est, 6 kilomètre heure."
        assert res.get('keepRunning', False) is True
        # Case unknow wind direction
        json['current_observation']['wind_dir'] = '...'
        res = dut.process({'location': 'Grenoble', 'weatherType': 'meteo'})
        assert res['speech'] == "Partiellement nuageux, 20 degrés, vent ..., 6 kilomètre heure."
        assert res.get('keepRunning', False) is True
        # Case no wind
        json['current_observation']['wind_kph'] = 0
        res = dut.process({'location': 'Grenoble', 'weatherType': 'meteo'})
        assert res['speech'] == "Partiellement nuageux, 20 degrés, pas de vent."
        assert res.get('keepRunning', False) is True

def testUnknownCity(dut):
    json = {"response":{"version":"0.1","termsofService":"http://www.wunderground.com/weather/api/d/terms.html","features":{"conditions":1},"error":{"type":"querynotfound","description":"No cities match your search query"}}}
    city = 'unknowCity'
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, json=json) 
        res = dut.process({'location': city, 'weatherType': 'meteo'})
        speech = res['speech']
        assert city in speech
        assert speech.replace(city, '/CITY/') in dut.text['FR']['cityNotFound']
        assert res.get('keepRunning', False) is False

def testError(dut):
    json = {"response":{"version":"0.1","termsofService":"http://www.wunderground.com/weather/api/d/terms.html","features":{"conditions":1},"error":{"type":"ohter","description":"No cities match your search query"}}}
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, json=json) 
        res = dut.process({'location': 'error', 'weatherType': 'meteo'})
        speech = res['speech']
        assert speech == 'Erreur du serveur météo.' 
        assert res.get('keepRunning', False) is False

def testKey(dut):
    jsonKeyError = {"response":{"version":"0.1","termsofService":"http://www.wunderground.com/weather/api/d/terms.html","features":{},"error":{"type":"keynotfound","description":"this key does not exist"}}}
    jsonKeyOk = {"response":{"version":"0.1","termsofService":"http://www.wunderground.com/weather/api/d/terms.html","features":{"conditions":1}},"current_observation":{"image":{"url":"http://icons.wxug.com/graphics/wu2/logo_130x80.png","title":"Weather Underground","link":"http://www.wunderground.com"},"display_location":{"full":"Grenoble, France","city":"Grenoble","state":"38","state_name":"France","country":"FR","country_iso3166":"FR","zip":"00000","magic":"254","wmo":"07487","latitude":"45.18999863","longitude":"5.73000002","elevation":"210.9"},"observation_location":{"full":"Grenoble, ","city":"Grenoble","state":"","country":"FR","country_iso3166":"FR","latitude":"45.36999893","longitude":"5.32999992","elevation":"1266 ft"},"estimated":{},"station_id":"LFLS","observation_time":"Last Updated on août 10, 17:30 CEST","observation_time_rfc822":"Thu, 10 Aug 2017 17:30:00 +0200","observation_epoch":"1502379000","local_time_rfc822":"Thu, 10 Aug 2017 17:49:03 +0200","local_epoch":"1502380143","local_tz_short":"CEST","local_tz_long":"Europe/Paris","local_tz_offset":"+0200","weather":"Partiellement nuageux","temperature_string":"68 F (20 C)","temp_f":68,"temp_c":20,"relative_humidity":"37%","wind_string":"From the ENE at 4 MPH","wind_dir":"ENE","wind_degrees":70,"wind_mph":4,"wind_gust_mph":0,"wind_kph":6,"wind_gust_kph":0,"pressure_mb":"1018","pressure_in":"30.06","pressure_trend":"0","dewpoint_string":"41 F (5 C)","dewpoint_f":41,"dewpoint_c":5,"heat_index_string":"NA","heat_index_f":"NA","heat_index_c":"NA","windchill_string":"NA","windchill_f":"NA","windchill_c":"NA","feelslike_string":"68 F (20 C)","feelslike_f":"68","feelslike_c":"20","visibility_mi":"6.2","visibility_km":"10.0","solarradiation":"--","UV":"2","precip_1hr_string":"-9999.00 in (-9999.00 mm)","precip_1hr_in":"-9999.00","precip_1hr_metric":"--","precip_today_string":"0.00 in (0.0 mm)","precip_today_in":"0.00","precip_today_metric":"0.0","icon":"partlycloudy","icon_url":"http://icons.wxug.com/i/c/k/partlycloudy.gif","forecast_url":"http://www.wunderground.com/global/stations/07487.html","history_url":"http://www.wunderground.com/history/airport/LFLS/2017/8/10/DailyHistory.html","ob_url":"http://www.wunderground.com/cgi-bin/findweather/getForecast?query=45.36999893,5.32999992","nowcast":""}}
    with requests_mock.Mocker() as m:
        m.get('http://api.wunderground.com/api/keyError/conditions/lang:FR/q/France/Grenoble.json', json=jsonKeyError)
        m.get('http://api.wunderground.com/api/keyOk/conditions/lang:FR/q/France/Grenoble.json', json=jsonKeyOk)
        dut.apiKey = 'keyOk'
        res = dut.process({'location': 'Grenoble', 'weatherType': 'meteo'})
        speech = res['speech']
        assert speech == "Partiellement nuageux, 20 degrés, vent d'Est, 6 kilomètre heure."
        assert res.get('keepRunning', False) is True 
        dut.apiKey = 'keyError'
        res = dut.process({'location': 'Grenoble', 'weatherType': 'meteo'})
        speech = res['speech']
        assert speech == 'Mauvaise clef API Wunderground.'
        assert res.get('keepRunning', False) is False
