import random
import psycopg2

def reinitialize():
	reinit_text = open("templates/original_game.html").read()
	with open("templates/game.html", "w") as f:
		f.write(reinit_text)
		
def toss():
	return random.randrange(1, 3)

def cardset():
	conn = psycopg2.connect("dbname = stat_database user = postgres password = postgres")
	c = conn.cursor()
	c.execute("SELECT * FROM base_table")
	player_list = c.fetchall()
	options = range(len(player_list))
	cardset1 = []
	cardset2 = []

	for i in xrange(21):
		random.shuffle(options)
		opt1 = options.pop()
		opt2 = options.pop(0)
		cardset1.append(player_list[opt1][1])
		cardset2.append(player_list[opt2][1])

	html_text = open("templates/game.html").read()
	new_html_text = html_text.replace("***tosswinner***", "Player " + str(toss()) + " won the toss, so he will get to start") \
					.replace("***player2***", "</div><div>".join(cardset2)) \
					.replace("***player1***", "</div><div>".join(cardset1)) \

	with open("templates/game.html", "w") as f:
		f.write(new_html_text)
