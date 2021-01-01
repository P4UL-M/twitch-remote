import TwitchRequest


async def helpCommands(websocket, CHAT, reponse):
    await websocket.send(f'PRIVMSG  #{CHAT} :Bienvenu sur le bot de la chaîne, les commandes disponnibles sont !discord(affiche le lien vers le discord de la chaîne), !viewers(affiche les viewers actuels)')
    print(f"Envoie de la réponse à !help ...")


async def discord(websocket, CHAT, reponse):
    await websocket.send(f'PRIVMSG #{CHAT} :https://discord.gg/jBYp2s6')
    print(f"Envoie de la réponse à !discord ...")


async def viewers(websocket, CHAT, reponse):
    viewers = ", ".join(TwitchRequest.myrequests.get_viewers())
    await websocket.send(f'PRIVMSG #{CHAT} :Les viewers actuels du chat sont : {viewers}.')
    print(f"Envoie de la réponse à !viewers ...")


async def bienvenu(websocket, CHAT, reponse):
    i = 1
    pseudo = str()
    while reponse[i] != "!":
        pseudo += reponse[i]
        i += 1
    await websocket.send(f'PRIVMSG #{CHAT} :salut 👋 {pseudo}!')
    print(f"Souhaite la bienvenu au nouveau viewer ...")

AllCommands = {
    ('!help'): helpCommands,
    ('!discord'): discord,
    ('!viewers'): viewers,
    ('yo', 'bjr', 'bonjour', 'bsr', 'bonsoir', 'slt', 'salut', 'hi'): bienvenu
}
