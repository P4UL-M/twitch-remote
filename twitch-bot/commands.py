
"""             DOC - Ajout des commandes de bot ici :
    ajout de la commande via nouvelle fonction, ensuite il faut la
    référencer avec son mot de détection dans le dictionaire en bas.
    la commande peut avoir plusieur mot clef
    la fonction est obligé de demandé le paramètre ctx
"""


async def helpCommands(ctx):
    await ctx.send('Bienvenu sur le bot de la chaîne, les commandes disponnibles sont !discord(affiche le lien vers le discord de la chaîne), !viewers(affiche les viewers actuels)')
    print(f"Envoie de la réponse à !help ...")


async def discord(ctx):
    await ctx.send('https://discord.gg/jBYp2s6')
    print(f"Envoie de la réponse à !discord ...")


async def viewers(ctx):
    viewers = ", ".join(ctx.viewers)
    await ctx.send(f'Les viewers actuels du chat sont : {viewers}.')
    print(f"Envoie de la réponse à !viewers ...")


async def bienvenu(ctx):
    i = 1
    pseudo = str()
    while ctx.content[i] != "!":
        pseudo += ctx.content[i]
        i += 1
    await ctx.send(f'salut 👋 {pseudo}!')
    print(f"Souhaite la bienvenu au nouveau viewer ...")

AllCommands = {
    ('!help'): helpCommands,
    ('!discord'): discord,
    ('!viewers'): viewers,
    ('yo', 'bjr', 'bonjour', 'bsr', 'bonsoir', 'slt', 'salut', 'hi'): bienvenu
}
