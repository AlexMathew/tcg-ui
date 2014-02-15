import psycopg2
import random
from flask import Flask, render_template
import setup_cardsets

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/rules')
def rules():
	return render_template('rules.html')
	
@app.route('/setup')
def setup():
	setup_cardsets.reinitialize()
	return render_template('setup.html')

@app.route('/game')
def game():
	setup_cardsets.cardset()
	return render_template('game.html')

if __name__ == '__main__':
	app.run()