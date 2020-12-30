import requests
import json
import time
from decouple import config


class request():
    def __init__(self, token, bot_id, token_type):
        self.token = token_type[0].upper() + token_type[1:] + " " + token
        self.id = bot_id
        self. headers = {'Client-Id': self.id,
                         'Authorization': self.token}

    def get_viewers(self):
        r = requests.get(
            'https://tmi.twitch.tv/group/user/le_picard_fr/chatters', headers=self.headers)
        rep = r.json()["chatters"]["viewers"] + [i for i in r.json()["chatters"]["moderators"]
                                                 if i != 'streamlabs']
        return rep

    def startpub(self):

        # demande de pub
        mydata = {
            'broadcaster_id': "222142107",
            'length': 60
        }
        r = requests.post(
            'https://api.twitch.tv/helix/channels/commercial', data=mydata, headers=self.headers)
        print(r.url)
        print(r.json())


myrequests = request(config('USER_TOKEN'), config(
    'USER_ID'), config('TOKEN_TYPE'))
