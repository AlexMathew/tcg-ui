from flask import Flask, render_template
from setup_cardsets import CardOperations

co = CardOperations()

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/rules')
def rules():
	return render_template('rules.html')
	
@app.route('/setup')
def setup():
	return render_template('setup.html')

@app.route('/toss')
def toss():
	co.cardset()
	return render_template('toss.html')

@app.route('/begin')
def begin():
	co.toss_result()
	return render_template('begin.html')

@app.route('/game')
def game():
	co.update_page()
	return render_template('game.html')

@app.route('/game/<int:statval>')
def game_move(statval):
	print statval
	co.update_page()
	return render_template('game.html')

if __name__ == '__main__':
	app.run()