import time
import asyncio
import websockets
from decouple import config
import TwitchRequest
import commands


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
                    # si vérification d'abonnement
                    if 'PING :tmi.twitch.tv' in str(reponse):
                        await websocket.send('PONG :tmi.twitch.tv')
                        print(f'Reconnection ...')
                    # si désabonnée
                    elif ':le_picard_fr!le_picard_fr@le_picard_fr.tmi.twitch.tv PART #le_picard_fr' in str(reponse):
                        print('deconnexion terminé !')
                        return
                    # si commande detectée
                    else:
                        await commands.run(self.socket, reponse)

    async def tearsdown(self):
        # demande de désabonnement
        await self.socket.send(f'PRIVMSG #{self.CHAT} :/me Deconnection en cours ...')
        await self.socket.send(f'PART #{self.CHAT}')
        print(f"Déconnexion du chat ...")


myChat = Bot()
