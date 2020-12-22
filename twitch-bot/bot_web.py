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
        # debug debut
        logging.info("Thread %s: starting", self.name)
        # try pour le raise exception
        try:
            a = bot_class.mybot.run()
            print(a)
        finally:
            logging.info("Thread %s: finishing", self.name)

    def get_id(self):
        # returns id of the respective thread
        for id, thread in threading._active.items():
            if thread is self:
                return id

    # fonction a appeller pour fermer le thread en cour
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')


# format pour debug special plus clair avec timer de ce qu'il ce passe
format = "%(asctime)s: %(message)s"
logging.basicConfig(
    format=format, level=logging.INFO, datefmt="%H:%M:%S")
# supression des log flask
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True


# fonction permettant de recuperer la variable globale
def get_thread(New=False):
    global t1
    if New:
        t1 = thread_with_exception('twitch_bot')
    try:
        return t1
    except NameError:
        return None


# sur requete AJAX _get_message
@app.route('/Le_Picard_Fr/twitch-bot/_get_message')
def get_message():
    param = request.args.get('param', 'pas de param', type=str)
    print("##### appel https:  " + param + " #####")
    if param == "demarer":
        t1 = get_thread()
        try:
            if t1.is_alive():
                print("##### bot deja lance ! #####")
                return jsonify(result='bot deja lance !')
        except:
            print("##### bot en lancement ! #####")
            t1 = get_thread(New=True)
            t1.start()
            return jsonify(result='bot lance a ' + str(time.strftime("%H:%M:%S")))
    if param == 'arret':
        t1 = get_thread()
        try:
            if t1.is_alive():
                # t1.raise_exception()
                print("##### arret du bot ! #####")
                return jsonify(result='bot arreter a ' + str(time.strftime("%H:%M:%S")))
        except:
            print("##### Erreur d'arret du bot ! #####")
            return jsonify(result="Erreur dans l'arret du bot, verifier que vousa vez deja lancer un bot")
    else:
        return jsonify(result='message imcompris : ' + param)


if __name__ == '__main__':
    # lancement de l'app
    app.run(
        host="localhost",
        port=int("82"),
        debug=True
    )
