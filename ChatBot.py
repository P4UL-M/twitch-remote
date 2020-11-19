import bot_class
import threading
import time
import logging
import ctypes


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


def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(10)
    # raise exception to stop the thread with the bot
    t1.raise_exception()
    logging.info("Thread %s: finishing", name)


if __name__ == "__main__":
    # format pour debug spécial plus clair avec timer de ce qu'il ce passe
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Main    : before creating thread")
    # création du thread, l'option daemon impose le thread à s'arrêter si le programme global arrive à sa fin
    x1 = threading.Thread(target=thread_function, args=(1,), daemon=True)
    t1 = thread_with_exception('twitch_bot')
    logging.info("Main    : before running thread")
    # lancement du thread
    t1.start()
    x1.start()
    logging.info("Main    : wait for the thread to finish")
    # la tache thread est maintenant effectué en premier plan, elle ne tourne plus en simultanées le programme attend la fin pour passer à la suite
    t1.join()
    logging.info("Main    : all done")
