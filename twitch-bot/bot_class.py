from twitchio.ext import commands
import sys
from decouple import config

BOT_TOKKEN = config('BOT_TOKKEN')
BOT_ID = config('BOT_ID')
BOT_NAME = config('BOT_NAME')


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=BOT_TOKKEN, client_id=BOT_ID,
                         nick=BOT_NAME, prefix='!', initial_channels=[BOT_NAME])

    # Connection
    async def event_ready(self):
        print(f'Ready | {self.nick} est online')
        global ws
        ws = mybot._ws
        await ws.send_privmsg(self.nick, f"/me le ChatBot est actuellement disponible !")

    # LOG :
    async def event_message(self, ctx):
        # ignore si le message viens de lui même
        if ctx.author.name.lower() == 'le_picard_fr'.lower():
            return
        # log
        print(ctx.content)
        # test d'analyse de message
        if ctx.content == 'message de test':
            # faire des trucs
            pass
        # renvoie du message vers les commandes
        await self.handle_commands(ctx)

    # Commande 'discord' :
    @commands.command(name='discord')
    async def discord(self, ctx):
        await ctx.send('https://discord.gg/jBYp2s6')

    # Commande 'test' :
    @commands.command(name='test')
    async def test(self, ctx):
        await ctx.send(f'👋 {ctx.author.name} !')

    # Commande 'pub' :
    @commands.command(name='pub')
    async def pub(self, ctx):
        print("vous avez demander une pub")
        await ctx.send("/commercial 60")
        await ctx.send("/pub 60")

    # Commande 'viewers' :
    @commands.command(name='viewers')
    async def viewers(self, ctx):
        interdit = ["streamlabs", "commanderroot",
                    "letsdothis_music", "lurxx", "vicarchurger", "thedevilisob", "rubberslayer", "princess_league", "cartierlogic"]
        chatters = await mybot.get_chatters(ctx.channel.name)
        elts = [i for i in chatters.all if i not in interdit]
        print("list = " + str(elts))
        await ctx.send("les viewers actuels sont : " + ", ".join(elts) + ".")


mybot = Bot()
