import time
import asyncio
import websockets
import sys
from decouple import config
import TwitchRequest


class Bot():
    def __init__(self, user, chat, token):
        self.USER = user
        self.CHAT = chat
        self.TOKEN = token

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
                message = "le ChatBot est actuellement disponible !"
                await websocket.send(f'PRIVMSG #{CHAT} :{message}')

                while(True):
                    time.sleep(0.5)
                    reponse = await websocket.recv()
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
                        message = "bienvenu sur le bot de la chaîne, les commandes disponnibles sont : !discord (affiche le lien vers le discord de la chaîne), !viewers (affiche les viewers actuels)"
                        await websocket.send(f'PRIVMSG #{CHAT} :{message}')
                        print(f"Envoie de la réponse ...")
                    elif '!discord' in str(reponse):
                        message = "https://discord.gg/jBYp2s6"
                        await websocket.send(f'PRIVMSG #{CHAT} :{message}')
                        print(f"Envoie de la réponse ...")
                    elif '!viewers' in str(reponse):
                        #message = TwitchRequest.get_viewers()
                        message = "en construction, ..."
                        await websocket.send(f'PRIVMSG #{CHAT} :{message}')
                        print(f"Envoie de la réponse ...")

    # test pour quitter le chat
    async def tearsdown(self):
        # demande de désabonnement
        await self.socket.send(f'PRIVMSG #{CHAT} :Deconnection en cours ...')
        await self.socket.send(f'PART #{self.CHAT}')
        print(f"Déconnexion du chat ...")


myChat = Bot(config('BOT_NAME'), config('BOT_NAME'), config('BOT_TOKKEN'))
