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
		self.salary = int(salary)
		self.team = team
		self.PPG = float(PPG)
		self.value = float(self.PPG)/(float(salary)/1000) 
	def printPlayer(self): 
		print(self.name, self.position, self.team, self.salary, self.PPG)
		
def createStarterLineup(qb_list, rb_list, wr_list, te_list, flex_list, dst_list): 
	#algorithm is to make the higehst PPG lineup and then examine each replacement 
	#at each role choosing the smallest decrease in salary as the actual change
	
	#0   1    2    3    4    5    6   7     9
	#QB, RB1, RB2, WR1, WR2, WR3, TE, FLEX, DST
	lineup = []
	salary = 50000
	positions_used = []
	
	#create stacked lineup
	lineup.append(qb_list[0])
	positions_used.append("QB")
	
	for i in range(2): 
		tmp = rb_list[i]
		lineup.append(tmp)
		positions_used.append("RB")
	for i in range(3): 
		tmp = wr_list[i]
		lineup.append(tmp)
		positions_used.append("WR")
	
	lineup.append(te_list[0])
	positions_used.append("TE")
	
	for i in range(len(flex_list)): 
		if flex_list[i] not in lineup: 
			lineup.append(flex_list[i])
			positions_used.append("FLEX")
			break
	
	lineup.append(dst_list[0])
	positions_used.append("DST")
	
	return lineup

def computeSalary(lineup): 
	sal = 0
	for player in lineup:
		sal += player.salary
	return sal
	
def scoreLineup(lineup): 
	score = 0
	for player in lineup: 
		score += player.PPG
	return score
	
def sortByValue(elem): 
	return elem.value
def sortByPPG(elem): 
	return elem.PPG
	
with open('DKSalaries10_11_19.csv') as csv_file: 
	csv_reader = csv.reader(csv_file, delimiter=",")
	line_count = 0
	for row in csv_reader: 
		if line_count == 0: 
			#print(f'Column names are {", ".join(row)}')
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
qb_list.sort(key=sortByPPG, reverse=True)
rb_list.sort(key=sortByPPG, reverse=True)
wr_list.sort(key=sortByPPG, reverse=True)
te_list.sort(key=sortByPPG, reverse=True)
flex_list.sort(key=sortByPPG, reverse=True)
dst_list.sort(key=sortByPPG, reverse=True)

lineup = createStarterLineup(qb_list, rb_list, wr_list, te_list, flex_list, dst_list)
for player in lineup: 
		player.printPlayer()
print(scoreLineup(lineup))
print(computeSalary(lineup))