import random
from player_stats import PlayerStats, stats_types

def compare_bbf(bbf1, bbf2):
	if not '/' in bbf1:
		if not '/' in bbf2:
			return True
		return False
	if not '/' in bbf2:
		return True
	
	w1, r1 = bbf1.split('/')
	w1, r1 = int(w1), int(r1)
	w2, r2 = bbf2.split('/')
	w2, r2 = int(w2), int(r2)

	if w1 > w2:
		return True
	elif w2 > w1:
		return False
	else:
		if r1 < r2:
			return True
		else:
			return False

def compare_with_id(stat_id, stat1, stat2):
	if int(stat1) == 0:
		return False
	elif int(stat2) == 0:
		return True
	else:
		pass
	if stat_id == 22 or stat_id == 23 or stat_id == 24:
		return stat1 < stat2
	return stat1 > stat2	

class CardOperations(object):

	def __init__(self):
		self.reset()

	def reset(self):
		self.in_ctrl = 0
		self.page_no = 0
		self.result = ""

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
		
		with open("templates/pages/begin.html", "w") as f:
			f.write(new_html_begin_text)

	def cardset(self, ps):
		self.ps = ps

	def update_page(self):
		p1 = self.ps.PlayerSet1[0]
		self.ps.PlayerSet1.rotate(-1)
		p2 = self.ps.PlayerSet2[0]
		self.ps.PlayerSet2.rotate(-1)

		if self.in_ctrl == 0:
			p = p1
			self.ctrl = p1
			self.vs = p2
		else:
			p = p2
			self.ctrl = p2
			self.vs = p1

		html_text = open("templates/original_game.html").read()

		new_html_text = html_text \
						.replace("***result***", '<div class="well">' + self.result + '</div>' if self.page_no else self.result) \
						.replace("***inctrl***", str(self.in_ctrl + 1)) \
						.replace("***playername***", str(p.name)) \
						.replace("***playerimg***", str(p.img_url))

		statline = '<li><a href="/game/***statlink***">***stat*** - ***value***</a></li>'

		stats = ""
		linker = 1

		for i in stats_types:
			stat = stats_types[i]
			if i==15 or i==17 or i==18:
				continue
			stats += statline \
					 .replace("***statlink***", str(linker*100 + i)) \
					 .replace("***stat***", stat.replace("_", " ").capitalize()) \
					 .replace("***value***", str(p.test[i]))

		for _ in xrange(2):
			stats += statline \
					 .replace("***statlink***", str(linker*100 + 27)) \
					 .replace("***stat***", "") \
					 .replace("***value***", "")

		new_html_text = new_html_text \
						.replace("***teststats***", stats)

		stats = ""
		linker = 2

		for i in stats_types:
			stat = stats_types[i]
			if i==15 or i==17 or i==18:
				continue
			stats += statline \
					 .replace("***statlink***", str(linker*100 + i)) \
					 .replace("***stat***", stat.replace("_", " ").capitalize()) \
					 .replace("***value***", str(p.odi[i]))

		for _ in xrange(2):
			stats += statline \
					 .replace("***statlink***", str(linker*100 + 27)) \
					 .replace("***stat***", "") \
					 .replace("***value***", "")

		new_html_text = new_html_text \
						.replace("***odistats***", stats)

		stats = ""
		linker = 3

		for i in stats_types:
			stat = stats_types[i]
			if i==15 or i==17 or i==18:
				continue
			stats += statline \
					 .replace("***statlink***", str(linker*100 + i)) \
					 .replace("***stat***", stat.replace("_", " ").capitalize()) \
					 .replace("***value***", str(p.t20[i]))

		for _ in xrange(2):
			stats += statline \
					 .replace("***statlink***", str(linker*100 + 27)) \
					 .replace("***stat***", "") \
					 .replace("***value***", "")

		new_html_text = new_html_text \
						.replace("***t20stats***", stats)

		with open("templates/pages/game.html", "w") as f:
			f.write(new_html_text) 

	def compare(self, stat):
		stat_class = int(stat / 100)
		stat_id = stat % 100
		if stat_class == 1:
			stat1 = self.ctrl.test[stat_id]
			stat2 = self.vs.test[stat_id]
			format = "Tests"
		elif stat_class == 2:
			stat1 = self.ctrl.odi[stat_id]
			stat2 = self.vs.odi[stat_id]
			format = "ODIs"
		else:
			stat1 = self.ctrl.t20[stat_id]
			stat2 = self.vs.t20[stat_id]
			format = "T20Is"
#		else:
#			stat1 = self.ctrl.fc[stat_id]
#			stat2 = self.vs.fc[stat_id]
#			format = "First Class cricket"
		
		if stat1 == stat2:
			self.result = "CLASH !!! " + self.ctrl.name + " and " + self.vs.name + " had a '" \
						  + stats_types[stat_id].replace("_", " ") + "' stat of " + str(stat1) + " for " + format + ".\n" \
						  + " Player " + str(self.in_ctrl + 1) + " go again and select another stat !"
			self.ps.PlayerSet1.rotate(1)			
			self.ps.PlayerSet2.rotate(1)
			return False

		self.result = self.ctrl.name + " had a '" + stats_types[stat_id].replace("_", " ") + "' stat of " + str(stat1) \
					  + " for " + format + ".\n" \
					  + "\nThe other player had " + self.vs.name + ", who had a '" + stats_types[stat_id].replace("_", " ") \
					  + "' stat of " + str(stat2) + " for " + format + ".\n"

		if type(stat1) == str:
			if compare_bbf(stat1, stat2):
				self.result += "YOU GOT HIS CARD !"
				if self.in_ctrl == 0:
					card = self.ps.PlayerSet2.pop()
					self.ps.PlayerSet1.append(card)
					if len(self.ps.PlayerSet2) == 0:
						return True
				else:
					card = self.ps.PlayerSet1.pop()
					self.ps.PlayerSet2.append(card)	
					if len(self.ps.PlayerSet1) == 0:
						return True
			else:
				self.result += "HE GOT YOUR CARD !"
				if self.in_ctrl == 0:
					card = self.ps.PlayerSet1.pop()
					self.ps.PlayerSet2.append(card)
					if len(self.ps.PlayerSet1) == 0:
						return True
				else:
					card = self.ps.PlayerSet2.pop()
					self.ps.PlayerSet1.append(card)	
					if len(self.ps.PlayerSet2) == 0:
						return True
				self.modify_ctrl((self.in_ctrl + 1) % 2)
		else:
			if compare_with_id(stat_id, stat1, stat2):
				self.result += "YOU GOT HIS CARD !"
				if self.in_ctrl == 0:
					card = self.ps.PlayerSet2.pop()
					self.ps.PlayerSet1.append(card)
					if len(self.ps.PlayerSet2) == 0:
						return True
				else:
					card = self.ps.PlayerSet1.pop()
					self.ps.PlayerSet2.append(card)	
					if len(self.ps.PlayerSet1) == 0:
						return True
			else:
				self.result += "HE GOT YOUR CARD !"
				if self.in_ctrl == 0:
					card = self.ps.PlayerSet1.pop()
					self.ps.PlayerSet2.append(card)
					if len(self.ps.PlayerSet1) == 0:
						return True
				else:
					card = self.ps.PlayerSet2.pop()
					self.ps.PlayerSet1.append(card)	
					if len(self.ps.PlayerSet2) == 0:
						return True
				self.modify_ctrl((self.in_ctrl + 1) % 2)

		return False

	def update_completion(self):
		html_text = open("templates/original_result.html").read()

		new_html_text = html_text \
						.replace("***result***", '<div class="well">' + self.result + '</div>') \
						.replace("***winner***", str(self.in_ctrl + 1))

		with open("templates/pages/result.html", "w") as f:
			f.write(new_html_text)