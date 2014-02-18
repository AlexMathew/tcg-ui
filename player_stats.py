import psycopg2
import random
from collections import deque

stats_types = {
			   1:"matches_played",
			   2:"innings_batted", 
			   3:"not_outs", 
			   4:"runs_scored", 
			   5:"highest_inns_score", 
			   6:"batting_average", 
			   7:"balls_faced", 
			   8:"batting_strike_rate", 
			   9:"hundreds_scored", 
			   10:"fifties_scored", 
			   11:"boundary_fours", 
			   12:"boundary_sixes", 
			   13:"catches_taken", 
			   14:"stumpings_made", 
			   15:"matches_played", 
			   16:"innings_bowled_in", 
			   17:"balls_bowled", 
			   18:"runs_conceded", 
			   19:"wickets_taken", 
			   20:"best_innings_bowling", 
			   21:"best_match_bowling", 
			   22:"bowling_average", 
			   23:"economy_rate", 
			   24:"bowling_strike_rate", 
			   25:"four_wkts_in_an_inns", 
			   26:"five_wkts_in_an_inns", 
			   27:"ten_wkts_in_a_match"
			   }

class Player(object):

	def __init__(self, name, img_url, test, odi, t20, fc):
		self.name = name
		self.img_url = img_url
		self.test = test
		self.odi = odi
		self.t20 = t20
		self.fc = fc

class PlayerStats(object):

	def __init__(self):
		self.indexset1, self.indexset2 = [], []
		self.PlayerSet1 = deque()
		self.PlayerSet2 = deque()

	def generate_cards(self):
		conn = psycopg2.connect("dbname = stat_database user = postgres password = postgres")
		c = conn.cursor()
		c.execute("SELECT * FROM base_table")
		player_list = c.fetchall()
		
		c.execute("SELECT * FROM test_stats")
		test_list = c.fetchall()
		c.execute("SELECT * FROM odi_stats")
		odi_list = c.fetchall()
		c.execute("SELECT * FROM t20i_stats")
		t20_list = c.fetchall()
		c.execute("SELECT * FROM fc_stats")
		fc_list = c.fetchall()
		
		options = range(len(player_list))

		for i in xrange(5):
			random.shuffle(options)
			
			opt1 = options.pop()
			self.indexset1.append(opt1)
			name1 = player_list[opt1][1]
			img_url1 = player_list[opt1][2]
			test1 = test_list[opt1]
			odi1 = odi_list[opt1]
			t201 = t20_list[opt1]
			fc1 = fc_list[opt1]
			player1 = Player(name1, img_url1, test1, odi1, t201, fc1)
			self.PlayerSet1.append(player1)

			opt2 = options.pop(0)
			self.indexset2.append(opt2)
			name2 = player_list[opt2][1]
			img_url2 = player_list[opt2][2]
			test2 = test_list[opt2]
			odi2 = odi_list[opt2]
			t202 = t20_list[opt2]
			fc2 = fc_list[opt2]
			player2 = Player(name2, img_url2, test2, odi2, t202, fc2)
			self.PlayerSet2.append(player2)
