from flask import Flask, render_template, request, jsonify
# script du bot de chat
import TwitchChat
# script du bot d'appel d'api
import TwitchRequest
# threading pour actionen arrière plan
import threading
import time
import logging


# Initialize the Flask application
app = Flask(__name__)


# format pour debug special plus clair avec timer de ce qu'il ce passe
format = "%(asctime)s: %(message)s"
logging.basicConfig(
    format=format, level=logging.INFO, datefmt="%H:%M:%S")
# supression des log flask
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True


# fonction permettant de recuperer la variable globale/d'en créer une nouvelle/de la supprimer (en dehors de l'autre car variable globale non dispo avec le décorateur)
def get_thread(New=False, delete=False):
    global t1
    if New:
        t1 = threading.Thread(target=TwitchChat.myChat.start, daemon=True)
    elif delete:
        del t1
        return True
    try:
        return t1
    except NameError:
        raise NameError


# sur requete AJAX _get_message
@app.route('/Le_Picard_Fr/twitch-bot/_get_message')
def get_message():
    # récupération des paramètre
    param = request.args.get('param', 'pas de param', type=str)
    token = request.args.get('token', type=str)
    token_type = request.args.get('token', type=str)[
        0].upper() + request.args.get('token', type=str)[1:]
    # envoie du tokken au script dépendant
    TwitchChat.myChat.USER_TOKEN = token_type + ' ' + token
    print("##### appel https:  " + param + " #####")
    # action en fonction du paramètre
    if param == "demarer":
        try:
            t1 = get_thread()
        except NameError:
            print("##### bot en lancement ! #####")
            t1 = get_thread(New=True)
            t1.start()
            return jsonify(result='bot lancé a ' + str(time.strftime("%H:%M:%S")))
        # si t1 existe
        print("##### bot déjà lancé ! #####")
        return jsonify(result='bot déjà lancé !')
    elif param == 'arret':
        try:
            t1 = get_thread()
        except NameError:
            print("##### Erreur d'arrêt du bot ! #####")
            return jsonify(result="Erreur dans l'arrêt du bot, vérifier que vous avez déjà lancé un bot")
        # si bot existe
        TwitchChat.myChat.stop()
        print("##### arrêt du bot ! #####")
        # suppresion de la variable maintenant inutile pour update les try, fait en global donc or du décorateur
        get_thread(delete=True)
        return jsonify(result='bot arrêté a ' + str(time.strftime("%H:%M:%S")))
    elif param == 'pub':
        TwitchRequest.myrequests.startpub(token)
        return jsonify(result="Demande de pub lancé")
    else:
        return jsonify(result='message imcompris : ' + param)


if __name__ == '__main__':
    # lancement de l'app
    app.run(
        host="localhost",
        port=int("82"),
        debug=True
    )
