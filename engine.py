import math
# percent of hands played with chen formula
# -1 1.0
# 0 0.9763313609467456
# 1 0.9230769230769231
# 2 0.8461538461538461
# 3 0.7337278106508875
# 4 0.5976331360946746
# 5 0.5029585798816568
# 6 0.31952662721893493
# 7 0.2485207100591716
# 8 0.14792899408284024
# 9 0.09467455621301775
# 10 0.0650887573964497
# 11 0.03550295857988166
# 12 0.029585798816568046
# 13 0.01775147928994083
# 14 0.01775147928994083
# 15 0.011834319526627219
# 16 0.011834319526627219
# 17 0.005917159763313609
# 18 0.005917159763313609
# 19 0.005917159763313609

def chen_percentages():
	for chen in range(-1, 20):
		count = 0
		for i in range(2, 15):
			for j in range(i, 15):
				if i != j and should_play((i, 'c'), (j, 'c'), 0, 0, chen):
					count += 1
				if should_play((i, 'c'), (j, 'a'), 0, 0, chen):
					count += 1
		print(chen, count/169)

# cards are represented as tuples with values [2, 14] and suits a character s, d, c, h
# num_players is an integer with the number of players
# position is your current position with the dealer being the 0th position
# strategy is a profile describing how tight/loose to play
def should_play(card1, card2, num_players, position, strategy):
	return chen_formula(card1, card2) >= strategy

def chen_value(card1, card2):
	rank = max(card1[0], card2[0])
	if rank == 14:
		return 10
	elif rank > 10:
		return rank-5
	else:
		return rank/2

def chen_connectors(card1, card2):
	gap = abs(card1[0] - card2[0])
	if gap <= 1:
		return 0
	elif gap <= 3:
		return -1 * (gap-1)
	elif gap == 4:
		return -4
	else:
		return -5

def chen_formula(card1, card2):
	value = chen_value(card1, card2)
	# pps
	if card1[0] == card2[0]:
		return max(5, value*2)
	# connector bonus
	if value <= 7 and abs(card1[0]-card2[0]) <= 2:
		value += 1

	if card1[1] == card2[1]:
		value += 2
	value += chen_connectors(card1, card2)
	return math.ceil(value)