import urllib
import random
import datetime
import sys
from bs4 import BeautifulSoup as Soup
import itertools

class TeamSet(object):

	def __init__(self):
		self.homepage_text = ""
		self.full_members = []

	def read_html_content(self):
		"""
		This method reads the HTML content from the Players list homepage on Cricinfo.
		"""
		print '\nEXTRACTING DATA..\n(The time taken depends on the speed of your Internet connection)\n'
		homepage_url = "http://espncricinfo.com/ci/content/player/index.html"
		try:
			uf = urllib.urlopen(homepage_url)
		except Exception:
			sys.exit("\nPlease turn on your Internet connection to continue.")
		self.homepage_text = uf.read()
			
	def generate_teams(self):
		"""
		This method parse the HTML of the page to extract the links to the various team pages.
		"""

		soup = Soup(self.homepage_text)
		li_set = soup.findAll('li')
		self.full_members = [(li_set[i+1].a.get('href'), li_set[i+1].text) 
							 for i, link in enumerate(li_set) if link.text == '|'][:10]



def key_fn(s):
	return s[1]


class PlayerSet(TeamSet):

	def __init__(self):
		self.player_list = []
		self.player_set = set()
		self.read_html_content()
		self.generate_teams()

	def generate_player_list(self):
		"""
		This method reads the HTML content of all the team pages, and uses HTML parsing
		to extract links to each individual players page.
		"""

		text = ""

		players = []
		
		for member in self.full_members:
			team_page_url = "http://espncricinfo.com" + member[0]
			try:
				uf = urllib.urlopen(team_page_url)
			except Exception:
				sys.exit("\nPlease turn on your Internet connection.")
			team_text = uf.read()
			soup = Soup(team_text)
			players.extend([("http://espncricinfo.com" + link.a.get('href'), link.text) 
							for link in soup.find(id = "rectPlyr_Playerlisttest").findAll('td')])
			team_path = complete_path + member[1] + ".txt"

		self.player_set = set(players)

		self.player_list = list(sorted(self.player_set, key = key_fn))

#		print 'TOTAL NUMBER OF PLAYERS : ', len(self.player_list)

		return self.player_list


class Game(object):

	def __init__(self):
		self.player1_cards = []
		self.player2_cards = []
		self.list_maker = PlayerSet()
		self.list_maker.generate_player_list()
		self.generate_card_sets()

	def generate_card_sets(self):
		"""
		From the Player list obtained from the generate_player_list() method of the PlayerSet class,
		randomly select players for the card sets for the two card holders.
		"""

		for i in xrange(21):
			random.shuffle(self.list_maker.player_list)
			self.player1_cards.append(self.list_maker.player_list.pop())

		random.shuffle(self.player1_cards)

		for i in xrange(21):
			random.shuffle(self.list_maker.player_list)
			self.player2_cards.append(self.list_maker.player_list.pop())

		random.shuffle(self.player2_cards)

	def display(self):
		"""
		Displays the card sets of the two card holders.
		"""

		print "\nCARD HOLDER 1 ==> "
		for card in self.player1_cards:
			print card[1]

		print "\nCARD HOLDER 2 ==> "
		for card in self.player2_cards:
			print card[1]

