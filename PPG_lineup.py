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
	#sort by PPG to get the OP lineup
	qb_list.sort(key=sortByPPG, reverse=True)
	rb_list.sort(key=sortByPPG, reverse=True)
	wr_list.sort(key=sortByPPG, reverse=True)
	te_list.sort(key=sortByPPG, reverse=True)
	flex_list.sort(key=sortByPPG, reverse=True)
	dst_list.sort(key=sortByPPG, reverse=True)

	#0   1    2    3    4    5    6   7     9
	#QB, RB1, RB2, WR1, WR2, WR3, TE, FLEX, DST
	lineup = []
	
	#create stacked lineup
	lineup.append(qb_list[0])
	
	for i in range(2): 
		tmp = rb_list[i]
		lineup.append(tmp)
	for i in range(3): 
		tmp = wr_list[i]
		lineup.append(tmp)
	
	lineup.append(te_list[0])
	
	for i in range(len(flex_list)): 
		if flex_list[i] not in lineup: 
			lineup.append(flex_list[i])
			break
	
	lineup.append(dst_list[0])
	
	return lineup

def iterateLineup(lineup, qb_list, rb_list, wr_list, te_list, flex_list, dst_list):
	#algorithm is to make the higehst PPG lineup and then examine each replacement 
	#at each role choosing the smallest decrease in salary as the actual change
	
	#get current positions of each player in list so we can look downwards
	current_qb = qb_list.index(lineup[0])
	current_rb1 = rb_list.index(lineup[1])
	current_rb2 = rb_list.index(lineup[2])
	current_wr1 = wr_list.index(lineup[3])
	current_wr2 = wr_list.index(lineup[4])
	current_wr3 = wr_list.index(lineup[5])
	current_te = te_list.index(lineup[6])
	current_flex = flex_list.index(lineup[7])
	current_dst = dst_list.index(lineup[8])
	
	
	downgrades = []
	downgrade_pos = -1
	for i in range(9): 
		if i==0:
			diff = checkDowngrade(current_qb, qb_list)
			downgrades.append(diff)
			downgrade_pos = i
		elif i==1:
			diff = checkDowngrade(current_rb1, rb_list)
			downgrades.append(diff)
			if diff < downgrades[downgrade_pos]: 
				downgrade_pos = i
		elif i==2:
			diff = checkDowngrade(current_rb2, rb_list)
			downgrades.append(diff)
			if diff < downgrades[downgrade_pos]: 
				downgrade_pos = i
		elif i==3:
			diff = checkDowngrade(current_wr1, wr_list)
			downgrades.append(diff)
			if diff < downgrades[downgrade_pos]: 
				downgrade_pos = i
		elif i==4:
			diff = checkDowngrade(current_wr2, wr_list)
			downgrades.append(diff)
			if diff < downgrades[downgrade_pos]: 
				downgrade_pos = i
		elif i==5:
			diff = checkDowngrade(current_wr3, wr_list)
			downgrades.append(diff)
			if diff < downgrades[downgrade_pos]: 
				downgrade_pos = i
		elif i==6:
			diff = checkDowngrade(current_te, te_list)
			downgrades.append(diff)
			if diff < downgrades[downgrade_pos]: 
				downgrade_pos = i
		elif i==7:
			diff = checkDowngrade(current_flex, flex_list)
			downgrades.append(diff)
			if diff < downgrades[downgrade_pos]: 
				downgrade_pos = i
		else: 
			diff = checkDowngrade(current_dst, dst_list)
			downgrades.append(diff)
			if diff < downgrades[downgrade_pos]: 
				downgrade_pos = i
	
	print(downgrades)
	print(downgrade_pos)
	
	#downgrade the lineup and call iterateLineup again
	if downgrade_pos ==0:
		lineup[downgrade_pos] = qb_list[current_qb+1]
	elif downgrade_pos ==1: 
		for i in range(len(rb_list)):
			if rb_list[current_rb1+i] not in lineup: 
				lineup[downgrade_pos] = rb_list[current_rb1+i]
				break
	elif downgrade_pos ==2: 
		for i in range(len(rb_list)):
			if rb_list[current_rb2+i] not in lineup: 
				lineup[downgrade_pos] = rb_list[current_rb2+i]
				break
	elif downgrade_pos ==3: 
		for i in range(len(wr_list)):
			if wr_list[current_wr1+i] not in lineup: 
				lineup[downgrade_pos] = wr_list[current_wr1+i]
				break
	elif downgrade_pos ==4: 
		for i in range(len(wr_list)):
			if wr_list[current_wr2+i] not in lineup: 
				lineup[downgrade_pos] = wr_list[current_wr2+i]
				break
	elif downgrade_pos ==5: 
		for i in range(len(wr_list)):
			if wr_list[current_wr3+i] not in lineup: 
				lineup[downgrade_pos] = wr_list[current_wr3+i]
				break
	elif downgrade_pos ==6: 
		for i in range(len(te_list)):
			if te_list[current_te+i] not in lineup: 
				lineup[downgrade_pos] = te_list[current_te+i]
				break
	elif downgrade_pos ==7: 
		for i in range(len(flex_list)):
			if flex_list[current_flex+i] not in lineup: 
				lineup[downgrade_pos] = flex_list[current_flex+i]
				break
	elif downgrade_pos ==8: 
		for i in range(len(dst_list)):
			if dst_list[current_dst+i] not in lineup: 
				lineup[downgrade_pos] = dst_list[current_dst+i]
				break
	return lineup
	
def checkDowngrade(idx, list): 
	cur_PPG = list[idx].PPG
	if idx+1 < len(list):
		next_PPG = list[idx+1].PPG
		return cur_PPG-next_PPG
	else: 
		return 100
	
	
def computeSalary(lineup): 
	sal = 0
	for player in lineup:
		sal += player.salary
	return sal

def printLineup(lineup):
	for player in lineup: 
		player.printPlayer()
	
def scoreLineup(lineup): 
	score = 0
	for player in lineup: 
		score += player.PPG
	return score
	
def sortBySalary(elem): 
	return elem.salary
	
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
	
lineup = createStarterLineup(qb_list, rb_list, wr_list, te_list, flex_list, dst_list)

#sort lists by salary so we can compare downgrades
qb_list.sort(key=sortBySalary, reverse=True)
rb_list.sort(key=sortBySalary, reverse=True)
wr_list.sort(key=sortBySalary, reverse=True)
te_list.sort(key=sortBySalary, reverse=True)
flex_list.sort(key=sortBySalary, reverse=True)
dst_list.sort(key=sortBySalary, reverse=True)

while computeSalary(lineup) > 50000:
	tmp = iterateLineup(lineup, qb_list, rb_list, wr_list, te_list, flex_list, dst_list)
	printLineup(tmp)
	print(computeSalary(tmp))
	print(scoreLineup(tmp))

#print(scoreLineup(lineup))
#print(computeSalary(lineup))

