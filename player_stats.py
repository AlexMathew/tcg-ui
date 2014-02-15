import psycopg2
import random
from collections import deque

stats_types = {
			   "matches_played_bat": 0,
			   "innings_batted": 1, 
			   "not_outs": 2, 
			   "runs_scored": 3, 
			   "highest_inns_score": 4, 
			   "batting_average": 5, 
			   "balls_faced": 6, 
			   "batting_strike_rate": 7, 
			   "hundreds_scored": 8, 
			   "fifties_scored": 9, 
			   "boundary_fours": 10, 
			   "boundary_sixes": 11, 
			   "catches_taken": 12, 
			   "stumpings_made": 13, 
			   "matches_played_bowl": 14, 
			   "innings_bowled_in": 15, 
			   "balls_bowled": 16, 
			   "runs_conceded": 17, 
			   "wickets_taken": 18, 
			   "best_innings_bowling": 19, 
			   "best_match_bowling": 20, 
			   "bowling_average": 21, 
			   "economy_rate": 22, 
			   "bowling_strike_rate": 23, 
			   "four_wkts_in_an_inns": 24, 
			   "five_wkts_in_an_inns": 25, 
			   "ten_wkts_in_a_match": 26
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

		for i in xrange(21):
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
