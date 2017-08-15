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
    json = {"response":{"version":"0.1","termsofService":"http://www.wunderground.com/weather/api/d/terms.html","features":{"conditions":1}},"current_observation":{"image":{"url":"http://icons.wxug.com/graphics/wu2/logo_130x80.png","title":"Weather Underground","link":"http://www.wunderground.com"},"display_location":{"full":"Fontaine, France","city":"Fontaine","state":"21","state_name":"France","country":"FR","country_iso3166":"FR","zip":"00000","magic":"363","wmo":"07270","latitude":"47.11999893","longitude":"4.44999981","elevation":"413.0"},"observation_location":{"full":"Rue de la Croix Amen de Fontainerot, Savilly, ","city":"Rue de la Croix Amen de Fontainerot, Savilly","state":"","country":"FR","country_iso3166":"FR","latitude":"47.124393","longitude":"4.273773","elevation":"1702 ft"},"estimated":{},"station_id":"ISAVILLY2","observation_time":"Last Updated on août 14, 20:25 CEST","observation_time_rfc822":"Mon, 14 Aug 2017 20:25:01 +0200","observation_epoch":"1502735101","local_time_rfc822":"Mon, 14 Aug 2017 20:31:37 +0200","local_epoch":"1502735497","local_tz_short":"CEST","local_tz_long":"Europe/Paris","local_tz_offset":"+0200","weather":"Ciel dégagé","temperature_string":"78.6 F (25.9 C)","temp_f":78.6,"temp_c":25.9,"relative_humidity":"55%","wind_string":"From the Est at 1.2 MPH Gusting to 3.1 MPH","wind_dir":"Est","wind_degrees":90,"wind_mph":1.2,"wind_gust_mph":"3.1","wind_kph":1.9,"wind_gust_kph":"5.0","pressure_mb":"1016","pressure_in":"30.01","pressure_trend":"0","dewpoint_string":"61 F (16 C)","dewpoint_f":61,"dewpoint_c":16,"heat_index_string":"NA","heat_index_f":"NA","heat_index_c":"NA","windchill_string":"NA","windchill_f":"NA","windchill_c":"NA","feelslike_string":"78.6 F (27 C)","feelslike_f":"78.6","feelslike_c":"27","visibility_mi":"N/A","visibility_km":"N/A","solarradiation":"--","UV":"-1","precip_1hr_string":"-999.00 in ( 0 mm)","precip_1hr_in":"-999.00","precip_1hr_metric":" 0","precip_today_string":"0.00 in (0 mm)","precip_today_in":"0.00","precip_today_metric":"0","icon":"clear","icon_url":"http://icons.wxug.com/i/c/k/clear.gif","forecast_url":"http://www.wunderground.com/global/stations/07270.html","history_url":"http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=ISAVILLY2","ob_url":"http://www.wunderground.com/cgi-bin/findweather/getForecast?query=47.124393,4.273773","nowcast":""}}
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, json=json)
        res = dut.process({'state': 'Côte'}, 'all', {'keepRunning': True, 'entities': {'weatherType': 'meteo', 'location': 'Fontaine'}})
        speech = res['speech']
        assert res.get('keepRunning', False) is True
        assert speech == 'Je ne trouve pas, quel département ?'
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, json=json)
        res = dut.process({'state': 'Vienne'}, 'all', {'keepRunning': True, 'entities': {'weatherType': 'meteo', 'location': 'Fontaine'}})
        speech = res['speech']
        assert res.get('keepRunning', False) is True
        assert speech == 'Je ne trouve pas, quel département ?'
    with requests_mock.Mocker() as m:
        m.get('http://api.wunderground.com/api/eb247d51126819a3/conditions/lang:FR/q/zmw:00000.363.07270.json', json=json)
        res = dut.process({'state': 'Côte d\'Or'}, 'all', {'keepRunning': True, 'entities': {'weatherType': 'meteo', 'location': 'Fontaine'}})
        speech = res['speech']
        assert res.get('keepRunning', False) is True
        assert speech == 'Ciel dégagé, 25.9 degrés, vent Est, 1.9 kilomètre heure.'

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
