YaJarvis - Yet Another Jarvis
=========

# Description
This software is my attempt to do a nice Jarvis, also called smart speaker :-)  
It will be used as standalone project on http or inside an [OpenJarvis](https://openjarvis.com) plugin.  

Technology underlying is Rasa NLU, based on Mitie and Spacy. Also, YaJarvis can answer several responses to a same question to feel more natural.


# Installation
Just use `setup.sh`, it will create a Python virtual environment and add required libraries, then install French libraries for Spacy.  

# Usage
1. Copy `plugins/weatherWunderground/config.sample.json` to `plugins/weatherWunderground/config.json` with your [Wunderground](https://www.wunderground.com/) API key and country.
2. Start Rasa NLU server thanks to `RasaNLU/runRasa.sh`.
3. Start YaJarvis thanks to `runYaJarvis.py`.
4. Done, you can try it with curl or in a browser `curl -G 'http://localhost:10001' --data-urlencode 'query=Quelle est la météo à Grenoble ?'`


Note: Do not forget to source the venv with `source venv/bin/activate`

# Training
The training file is really small for now and only in French. You can edit `RasaNLU/data/jarvis.json` to translate or improve it (PR are wellcome !), then run `data/trainModel.sh` to train RasaNLU.

# Exemple
It supports basic conversations:
```
You: What's the wether like ?
YaJarvis: In which city ?
You: Fontaine
YaJarvis: I found several cities, in which state ? Isère, Aube, Ain.
You: Isère
YaJarvis: Clear sky, 24 degrees, light North wind 6 kilometers by hour.
You: Waht about tomorrow ?
YaJarvis: Cloudy weather, from 18 to 27 degrees.
```
```
Vous: Quelle est la météo ?
YaJarvis: Dans quelle ville ?
Vous: Fontaine
YaJarvis: Plusieurs villes trouvées, dans quel département ? Isère, Aube, Ain.
Vous: Isère
YaJarvis: Ciel dégagé, 24 degrés, vent de nord 6 kilomètres heures.
Vous: Et demain ?
YaJarvis: Beau temps, de 18 à 27 degrés.
```
