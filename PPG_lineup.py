#program to analyze draftkings salaries
import csv

# class Game: 
	# def __init__(self, home, away, date, time)

player_list = []
qb_list = []
rb_list = []
wr_list = []
flex_list = []
te_list = []
dst_list = []

class Player: 
	def __init__(self, name, position, salary, team, PPG):
		self.name = name
		self.position = position
		self.salary = salary
		self.team = team
		self.PPG = PPG
		self.value = self.PPG/(salary/1000) 
	def printPlayer(self): 
		print(self.name, self.position, self.team, self.salary, self.PPG)
		
def createLineup(qb_list, rb_list, wr_list, te_list, flex_list, dst_list): 
	lineup = []
	#choose QB, starting with the best PPG per dollar
	
def scoreLineup(lineup): 
	score = 0
	for player in lineup: 
		score += player.PPG
	return score
	
def sortByValue(elem): 
	return elem.value
	
with open('DKSalaries10_11_19.csv') as csv_file: 
	csv_reader = csv.reader(csv_file, delimiter=",")
	line_count = 0
	for row in csv_reader: 
		if line_count == 0: 
			print(f'Column names are {", ".join(row)}')
			line_count += 1
		else:
			if row[0] == "DST": 
				tmp = Player(row[2][:-1], row[0], row[5], row[7], row[8])
				player_list.append(tmp)
				dst_list.append(tmp)
			else: 
				tmp = Player(row[2], row[0], row[5], row[7], row[8])
				player_list.append(tmp)
				if tmp.position == "RB": 
					rb_list.append(tmp)
					flex_list.append(tmp)
				elif tmp.position == "WR": 
					wr_list.append(tmp)
					flex_list.append(tmp)
				elif tmp.position == "TE": 
					te_list.append(tmp)
					flex_list.append(tmp)
				elif tmp.position == "QB":
					qb_list.append(tmp)
			line_count += 1
	#print(f'Processed {line_count} lines.')
	
#sort list by PPG and create lineup
player_list.sort(key=lambda elem: (elem.position, elem.value), reverse=True)
qb_list.sort(key=sortByValue, reverse=True)
rb_list.sort(key=sortByValue, reverse=True)
wr_list.sort(key=sortByValue, reverse=True)
te_list.sort(key=sortByValue, reverse=True)
flex_list.sort(key=sortByValue, reverse=True)
dst_list.sort(key=sortByValue, reverse=True)

for elem in player_list: 
	elem.printPlayer()


