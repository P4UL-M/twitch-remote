import requests
import json
import time
from decouple import config


class request():
    def __init__(self, bot_id):
        self.id = bot_id

    def get_viewers(self, token):
        self.headers = {
            'Client-Id': self.id,
            'Authorization': token
        }
        # requête des utilisateurs
        r = requests.get(
            'https://tmi.twitch.tv/group/user/le_picard_fr/chatters', headers=self.headers)
        rep = r.json()["chatters"]["viewers"] + [i for i in r.json()["chatters"]["moderators"]
                                                 if i != 'streamlabs']
        return rep

    def startpub(self, token):
        self.headers = {
            'Client-Id': self.id,
            'Authorization': 'Bearer ' + token
        }
        # demande de pub
        mydata = {
            'broadcaster_id': "222142107",
            'length': 60
        }
        r = requests.post(
            'https://api.twitch.tv/helix/channels/commercial', data=mydata, headers=self.headers)
        print(r.json())


myrequests = request(config(
    'USER_ID'))
