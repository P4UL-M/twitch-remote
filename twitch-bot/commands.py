# pour ajouter des commande il suffit d'ajouter une condition ici
async def run(websocket, reponse):
    if '!help' in str(reponse):
        await websocket.send(f'PRIVMSG  # {self.CHAT} :Bienvenu sur le bot de la chaîne, les commandes disponnibles sont: !discord(affiche le lien vers le discord de la chaîne), !viewers(affiche les viewers actuels)')
        print(f"Envoie de la réponse à !help ...")

    if '!discord' in str(reponse):
        await websocket.send(f'PRIVMSG #{self.CHAT} :https://discord.gg/jBYp2s6')
        print(f"Envoie de la réponse à !discord ...")

    if '!viewers' in str(reponse):
        viewers = ", ".join(
            TwitchRequest.myrequests.get_viewers(self.USER_TOKEN))
        await websocket.send(f'PRIVMSG #{self.CHAT} :Les viewers actuels du chat sont : {viewers}.')
        print(f"Envoie de la réponse à !viewers ...")

    # récupère seulement le text de la réponse sous forme d'array de mots
    reponse_ajust = reponse.replace(':', '').replace(
        '\r', '').replace('\n', '').split(" ")
    expresion = ['yo', 'bjr', 'bonjour',
                 'bsr', 'bonsoir', 'slt', 'salut', 'hi']
    if any(i for i in expresion if i in reponse_ajust):
        i = 1
        pseudo = str()
        while reponse[i] != "!":
            pseudo += reponse[i]
            i += 1
        await websocket.send(f'PRIVMSG #{self.CHAT} :salut 👋 {pseudo}!')
        print(f"Souhaite la bienvenu au nouveau viewer ...")
