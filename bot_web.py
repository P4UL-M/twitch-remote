from flask import Flask, render_template, request, jsonify
import bot_class
import threading
import time
from time import strftime
import logging
import ctypes


# Initialize the Flask application
app = Flask(__name__)


# class pour thread annulable : twitch_bot
class thread_with_exception(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self, daemon=True)
        self.name = name

    def run(self):
        # débug début
        logging.info("Thread %s: starting", self.name)
        # try pour le raise exception
        try:
            bot_class.mybot.run()
        finally:
            logging.info("Thread %s: finishing", self.name)

    def get_id(self):

        # returns id of the respective thread
        for id, thread in threading._active.items():
            if thread is self:
                return id

    # fonction à appeller pour fermer le thread en cour

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')


# format pour debug spécial plus clair avec timer de ce qu'il ce passe
format = "%(asctime)s: %(message)s"
logging.basicConfig(
    format=format, level=logging.INFO, datefmt="%H:%M:%S")
# création du thread, l'option daemon impose le thread à s'arrêter si le programme global arrive à sa fin
t1 = thread_with_exception('twitch_bot')


# fonction permettant de récupérer la variable globale
def get_thread(New=False):
    global t1
    if New:
        t1 = thread_with_exception('twitch_bot')
    return t1


# Route that will process the AJAX request, sum up two
# integer numbers (defaulted to zero) and return the
# result as a proper JSON response (Content-Type, etc.)
@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

# sur requete AJAX _get_message on renvoie le texte
# je suis la réponse ajax du serveur à + le paramètre transmis


@app.route('/_get_message')
def get_message():
    param = request.args.get('param', 'pas de param', type=str)
    print("##### appel https: starting, " + param + " #####")
    if param == "demarer":
        try:
            t1 = get_thread()
            if t1.is_alive():
                print("##### bot déjà lancé ! #####")
                return jsonify(result='bot déjà lancé !')
            else:
                print("##### bot non lancé ! #####")
                raise Exception("bot non lancé")
        except:
            t1 = get_thread(New=True)
            t1.start()
            return jsonify(result='bot lancé à ' + str(time.strftime("%H:%M:%S")))
    if param == 'arret':
        t1 = get_thread()
        try:
            if t1.is_alive():
                t1.raise_exception()
                print("##### arrêt du bot ! #####")
                return jsonify(result='bot arreter à ' + str(time.strftime("%H:%M:%S")))
            else:
                raise Exception("aucun bot lancé")
        except:
            print("##### Aucun bot lancé ! #####")
            return jsonify(result='aucun bot lancé')
    else:
        return jsonify(result='message imcompris ou bot non démarer : ' + param)


if __name__ == '__main__':
    # lancement de l'app
    app.run(
        host="localhost",
        port=int("82")
    )
