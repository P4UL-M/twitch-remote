import time
import asyncio
import websockets
import sys
from decouple import config
import TwitchRequest


class Bot():
    def __init__(self, user=config('BOT_NAME'), chat=config('BOT_NAME'), token=config('BOT_TOKKEN')):
        self.USER = user
        self.CHAT = chat
        self.TOKEN = token
        self.USER_TOKEN = None

    def start(self):
        asyncio.run(self.run())

    def stop(self):
        asyncio.run(self.tearsdown())

    async def run(self):
        uri = "wss://irc-ws.chat.twitch.tv:443"
        async with websockets.connect(uri) as websocket:
            self.socket = websocket
            # connection au serveur
            await websocket.send(f'PASS {self.TOKEN}')
            await websocket.send(f'NICK {self.USER}')
            print(f"Connection ...")

            reponse = await websocket.recv()

            # connection au chat
            await websocket.send(f'JOIN #{self.CHAT}')
            print(f"Connection au chat ...")

            time.sleep(1)

            reponse = await websocket.recv()

            # si connecté alors run en continu
            if ':le_picard_fr!le_picard_fr@le_picard_fr.tmi.twitch.tv JOIN #le_picard_fr' in str(reponse):
                await websocket.send(f'PRIVMSG #{self.CHAT} :/me le ChatBot est actuellement disponible !')

                while(True):
                    time.sleep(0.5)
                    reponse = await websocket.recv()
                    # récupère seulement le text de la réponse sous forme d'array de mots
                    reponse_ajust = reponse.replace(':', '').replace(
                        '\r', '').replace('\n', '').split(" ")
                    expresion = ['yo', 'bjr', 'bonjour',
                                 'bsr', 'bonsoir', 'slt', 'salut', 'hi']
                    # si vérification d'abonnement
                    if 'PING :tmi.twitch.tv' in str(reponse):
                        await websocket.send('PONG :tmi.twitch.tv')
                        print(f'Reconnection ...')
                    # si désabonnée
                    elif ':le_picard_fr!le_picard_fr@le_picard_fr.tmi.twitch.tv PART #le_picard_fr' in str(reponse):
                        print('deconnexion terminé !')
                        return
                    # si commande detectée
                    elif '!help' in str(reponse):
                        message = "/me bienvenu sur le bot de la chaîne, les commandes disponnibles sont : !discord (affiche le lien vers le discord de la chaîne), !viewers (affiche les viewers actuels)"
                        await websocket.send(f'PRIVMSG #{self.CHAT} :{message}')
                        print(f"Envoie de la réponse à !help ...")
                    elif '!discord' in str(reponse):
                        message = "https://discord.gg/jBYp2s6"
                        await websocket.send(f'PRIVMSG #{self.CHAT} :{message}')
                        print(f"Envoie de la réponse à !discord ...")
                    elif '!viewers' in str(reponse):
                        message = "les viewers actuels du chat sont : "
                        message += ", ".join(
                            TwitchRequest.myrequests.get_viewers(self.USER_TOKEN))
                        await websocket.send(f'PRIVMSG #{self.CHAT} :{message}')
                        print(f"Envoie de la réponse à !viewers ...")
                    elif any(i for i in expresion if i in reponse_ajust):
                        i = 1
                        pseudo = str()
                        while reponse[i] != "!":
                            pseudo += reponse[i]
                            i += 1
                        message = "salut 👋 " + pseudo + "!"
                        await websocket.send(f'PRIVMSG #{self.CHAT} :{message}')
                        print(f"Souhaite la bienvenu au nouveau viewer ...")
                    else:
                        print(reponse)

    # test pour quitter le chat
    async def tearsdown(self):
        # demande de désabonnement
        await self.socket.send(f'PRIVMSG #{self.CHAT} :/me Deconnection en cours ...')
        await self.socket.send(f'PART #{self.CHAT}')
        print(f"Déconnexion du chat ...")


myChat = Bot()
