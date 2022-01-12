import requests
import json
import time
# -------------------------
# Jinja2
# -------------------------
from jinja2 import Environment, FileSystemLoader
template_dir = 'Templates/'
env = Environment(loader=FileSystemLoader(template_dir))
xmen_template = env.get_template('XMen.j2')

# -------------------------
# Headers
# -------------------------
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
}

# -------------------------
# All Characters
# -------------------------

person_template = env.get_template('character.j2')
people = requests.request("GET", "https://xmenapiheroku.herokuapp.com/api/characters", headers=headers)
peopleJSON = people.json()
peopleList = peopleJSON['results']
while peopleJSON['info']['next']:
    people = requests.request("GET", peopleJSON['info']['next'], headers=headers)
    peopleJSON = people.json()
    peopleList.extend(peopleJSON["results"])

peoplePersonList = []
for person in peopleList:
    singlePersonJSON = person
    if singlePersonJSON not in peoplePersonList:
        peoplePersonList.append(singlePersonJSON)

# -------------------------
# Person Template
# -------------------------

    parsed_all_output = person_template.render(
        singlePerson = singlePersonJSON,
        )

# -------------------------
# Save Characters File
# -------------------------

    with open(f"Cerebro/Characters/{ singlePersonJSON['name'] }.md", "w") as fh:
        fh.write(parsed_all_output)                
        fh.close()

# -------------------------
# All Episodes
# -------------------------

episode_template = env.get_template('episode.j2')
episode = requests.request("GET", "https://xmenapiheroku.herokuapp.com/api/episodes", headers=headers)
episodeJSON = episode.json()
episodeList = episodeJSON['results']
while episodeJSON['info']['next']:
    episode = requests.request("GET", episodeJSON['info']['next'], headers=headers)
    episodeJSON = episode.json()
    episodeList.extend(episodeJSON["results"])

episodeEpisodeList = []
for episode in episodeList:
    episodeJSON = episode
    if episodeJSON not in episodeEpisodeList:
        episodeEpisodeList.append(episodeJSON)

# -------------------------
# Episode Template
# -------------------------

    parsed_all_output = episode_template.render(
        singleEpisode = episodeJSON,
        )

# -------------------------
# Save Characters File
# -------------------------

    with open(f"Cerebro/Episodes/{ episodeJSON['title'] }.md", "w") as fh:
        fh.write(parsed_all_output)                
        fh.close()

# -------------------------
# X-Men TAS Template
# -------------------------

parsed_all_output = xmen_template.render(
    peoplePersonList = peoplePersonList,
    episodeEpisodeList = episodeEpisodeList
    )

# -------------------------
# Save X-Men TAS File
# -------------------------

with open("Cerebro/X-Men The Animated Series.md", "w") as fh:
    fh.write(parsed_all_output)               
    fh.close()        