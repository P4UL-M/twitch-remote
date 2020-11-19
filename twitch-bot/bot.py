from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

#peut etre en cas de dossier partager avec apache
#@app.route('/')
#def index():
#    return render_template('index.html')

#normalement utilise avec json mais n'a pas l'air d'etre utile
#@app.route('/_add_numbers')
#def add_numbers():
#    a = request.args.get('a', 0, type=int)
#    b = request.args.get('b', 0, type=int)
#    return jsonify(result=a + b)


@app.route('/Le_Picard_Fr/twitch-bot/_get_message')
def get_message():
    param = request.args.get('param', 'pas de param', type=str)
    return jsonify(result='vous venez de m\'envoyer  ' + param)


if __name__ == '__main__':
    app.run(
        host="localhost",
        port=int("82"),
	    debug=True
    )

