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

@app.route('/toss/<int:cardcount>')
def toss(cardcount):
	co.cardset(cardcount)
	return render_template('toss.html')

@app.route('/begin')
def begin():
	co.toss_result()
	return render_template('begin.html')

@app.route('/game')
def game():
	co.update_page()
	co.page_no = 1
	return render_template('game.html')

@app.route('/game/<statval>')
def game_move(statval):
	try:
		completed = co.compare(int(statval))
		if not completed:
			co.update_page()
			return render_template('game.html')
		else:
			co.update_completion()
			return render_template('result.html')
	except Exception as detail:
		print detail

if __name__ == '__main__':
	app.run()