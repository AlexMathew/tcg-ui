import random
from player_stats import PlayerStats

class CardOperations(object):

	def __init__(self):
		self.in_ctrl = 0
		return

	def modify_ctrl(self, new_ctrl):
		self.in_ctrl = new_ctrl

	def toss(self):
		self.in_ctrl = random.randrange(0, 2)

	def toss_result(self):
		self.toss()
		html_begin_text = open("templates/original_begin.html").read()
		new_html_begin_text = html_begin_text \
							  .replace("***tosswinner***", "Player " + str(self.in_ctrl + 1) \
							  			+ " won the toss, so he will get to start") 
		
		with open("templates/begin.html", "w") as f:
			f.write(new_html_begin_text)

	def cardset(self):
		self.ps = PlayerStats()
		self.ps.generate_cards()

	def update_page(self):
		p1 = self.ps.PlayerSet1[0]
		self.ps.PlayerSet1.rotate(-1)
		p2 = self.ps.PlayerSet2[0]
		self.ps.PlayerSet2.rotate(-1)

		if self.in_ctrl == 0:
			p = p1
		else:
			p = p2

		html_text = open("templates/original_game.html").read()
		new_html_text = html_text \
						.replace("***inctrl***", str(self.in_ctrl + 1)) \
						.replace("***playername***", str(p.name)) \
						.replace("***playerimg***", str(p.img_url))

		with open("templates/game.html", "w") as f:
			f.write(new_html_text) 

		self.modify_ctrl(random.randrange(0, 2))