from engine import should_play
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep

def sound():
	print('\a')
	sleep(.3)
	print('\a')

def get_value(value):
	value = value.lower()
	if value == 'a':
		return 14
	elif value == 'k':
		return 13
	elif value == 'q':
		return 12
	elif value == 'j':
		return 11
	else:
		return int(value)

def get_strategy():
	strat = open('strategy.txt')
	chen_score = int(strat.read().strip())
	strat.close()
	return chen_score

# initialize
link = input("Paste Link Here: ").strip()
chen_score = get_strategy()

opts = Options()
driver = Chrome(options=opts)
driver.set_window_size(1000, 800)
driver.set_window_position(0, 0)
driver.get(link)
input("Press enter after joining the game.")
page_soup = BeautifulSoup(driver.page_source, 'html.parser')

while (True):
	print('new hand')
	# wait for fold option to indicate game start
	while not page_soup.select_one('button.fold'):
		sleep(1)
		page_soup = BeautifulSoup(driver.page_source, 'html.parser')
	is_bb = False
	# if there are no table cards we're on preflop
	print('starting')
	if page_soup.select_one('.table-cards') and len(page_soup.select_one('.table-cards').contents) == 0:
		new_chen_score = get_strategy()
		if chen_score != new_chen_score:
			chen_score = new_chen_score
			print('updated strategy with chen score: ' + str(chen_score))
		# get the player element
		player = page_soup.select_one('.table-player-1')
		# if there are not two cards, something is broken
		if len(player.select('.value')) != 2:
			sound()
			print('Did not find two hole cards!')
			continue
		# pull suits and values and zip them to create card objects
		suits = [ele.text for ele in player.select('.suit')]
		values = [get_value(ele.text) for ele in player.select('.value')]
		cards = list(zip(values, suits))
		# compute engine score
		if should_play(cards[0], cards[1], None, None, chen_score):
			sound()
			print('play', cards)
		else:
			print('fold')
			# if we're big blind and should fold
			if page_soup.select_one('button.check-fold'):
				try:
					driver.find_element_by_css_selector('button.check-fold').click()
					is_bb = True
				except:
					sound()
					print("Error! Couldn't fold!")
			else:
				try:
					driver.find_element_by_css_selector('button.fold').click()
				except:
					sound()
					print("Error! Couldn't fold!")
		last_cards = cards
	print('done with preflop, waiting on hand to finish')
	reached_flop = False
	while True:
		page_soup = BeautifulSoup(driver.page_source, 'html.parser')
		if reached_flop:
			if is_bb and page_soup.select_one('button.fold'):
				sound()
				print('reached flop checking bb')
				is_bb = False
			if page_soup.select_one('p.table-pot-size').text == '0':
				print('pot 0')
				break
		else:
			if page_soup.select_one('.show-your-hand'):
				break
			if page_soup.select_one('.table-cards') and len(page_soup.select_one('.table-cards').contents) != 0:
				reached_flop = True
		sleep(.8)
	print('hand finished')