import os
import random
import time
import keyboard
import sys
import select
import tty
import termios
import atexit
import colorama
from select import select

class KBHit:

    def __init__(self):
        '''Creates a KBHit object that you can call to do various keyboard things.
        '''
        # Save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)

        # New terminal setting unbuffered
        self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

        # Support normal-terminal reset at exit
        atexit.register(self.set_normal_term)


    def set_normal_term(self):
        ''' Resets to normal terminal.  On Windows this is a no-op.
        '''
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


    def getch(self):
        ''' Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        '''

        s = ''
        return sys.stdin.read(1)

    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.
        '''

        dr,dw,de = select([sys.stdin], [], [], 0)
        return dr != []




# 1 - free field
# 9 - frame
# 2 - moving block
# 3 - dead block
# 4 - block shadow


width = 10
height = 30
block_generated = 0
score = 0
block_position = ""

board = [[1 for x in range(width)] for y in range(height)]

def block_shadow(mode):
	if mode == "show":
		for a in range(height-1, 0, -1):
			for b in range(1, width-1, 1):
				element = board[a][b]
				if element == 2:
					for row in range(height-1, a, -1):
						if board[row][b] == 1:
							board[row][b] = 4
							break
	elif mode == "hide":
		for a in range(height-1, 0, -1):
			for b in range(1, width-1, 1):
				element = board[a][b]
				if element == 4:
					board[a][b] = 1

		#[el = 1 for el in board if el == 4]




def rotate_block(block_type):
	block_rotated = 0
	global block_position
	if block_type == '2liner':
		#print(block_position)
		if block_position == "vertical":
			for x in range(1, height-1, 1):
				for y in range(1, width-1, 1):
					element = board[x][y]
					if element == 2:
						#board[x][y] = 1
						board[x+1][y] = 1
						board[x][y+1] = 2
						block_rotated = 1
						block_position = "horizontal"
						break
				if block_rotated:
					break
		if block_position == "horizontal":
			for x in range(1, height-1, 1):
				for y in range(1, width-1, 1):
					if board[x][y] == 2:
						board[x][y+1] = 1
						board[x+1][y] = 2
						block_rotated = 1
						block_position = "vertical"
						break
				if block_rotated:
					break

	elif block_type == "L_block":
		if block_position == "1":
			for x in range(1, height-1, 1):
				for y in range(1, width-1, 1):
					element = board[x][y]
					if element == 2:
						board[x+1][y+1] = 1
						board[x][y+1] = 2
						block_rotated = 1
						block_position = "2"
						break
					if block_rotated:
						break
		elif block_position == "2":
			for x in range(1, height-1, 1):
				for y in range(1, width-1, 1):
					element = board[x][y]
					if element == 2:
						board[x+1][y] = 1
						board[x+1][y+1] = 2
						block_rotated = 1
						block_position = "3"
						break
					if block_rotated:
						break
		elif block_position == "3":
			for x in range(1, height-1, 1):
				for y in range(1, width-1, 1):
					element = board[x][y]
					if element == 2:
						board[x][y+1] = 1
						board[x+1][y] = 2
						block_rotated = 1
						block_position = "1"
						break
					if block_rotated:
						break








def score_check():

	rows_to_delete = list()
	for x in range(1, height-1, 1):
		row_check = 1
		for y in range(1, width-1, 1):
			element = board[x][y]
			if element != 3:
				row_check = 0
				break
		if row_check:
			rows_to_delete.append(x)

	print(rows_to_delete)

	for row in rows_to_delete:
		for y in range(1, width-1, 1):
			board[row][y] = 1
		for x in range(row, 0, -1):
			for y in range(1, width-1, 1):
				element = board[x][y]
				if element == 3:
					board[x][y] = 1
					board[x+1][y] = 3

	return len(rows_to_delete)
			

def horizontal_control(direction):
	if direction == "a":
		move_block_horizontal("left")
	elif direction == "d":
		move_block_horizontal("right")

def move_block_horizontal(direction):
	for x in range(1, height-1, 1):
		if direction == "left":
			for y in range(1, width-1, 1):
			#for y in range(width-1, 1, -1):
				element = board[x][y]
				if element == 2: #and move_possible_check("left"): #board[x][y-1] != 9:
					#cords = "%s %s" % (x, y)
					#print(cords)
			#	if direction == "left":
					board[x][y] = 1
					board[x][y-1] = 2
			#	elif direction == "right":
			#		board[x][y] = 1
			#		board[x][y+1] = 2
				#else: break
		elif direction == "right":
			for y in range(width-1, 0, -1):
			#for y in range(1, width-1, 1):
				element = board[x][y]
				if element == 2:  #and move_possible_check("right"): #board[x][y+1] != 9:
					cords = "%s %s" % (x, y)
					print(cords)
					board[x][y] = 1
					board[x][y+1] = 2
				#else: break

def move_possible_check(direction):
	check = 1
	"""for x in range(height-1, 0, -1):
		for y in range(1, width-1, 1):
			element = board[x][y]
			if element == 2:
				if direction == 'down':
					if board[x+1][y] == 9 or board[x+1][y] == 3:
						check = 0
				elif direction == "left":
					if board[x][y-1] == 9 or board[x][y-1] == 3: #or board[x][y-1] == 2:
						check = 0
				elif direction == "right":
					if board[x][y+1] == 9 or board[x][y+1] == 3: #or board[x][y+1] == 2:
						check = 0
						"""
	if direction == 'down':
		for x in range(height-1, 0, -1):
			for y in range(1, width-1, 1):
				element = board[x][y]
				if element == 2:
					if board[x+1][y] == 9 or board[x+1][y] == 3:
						check = 0
	elif direction == 'left':
		for x in range(height-1, 0, -1):
			if board[x][1] == 2:
				check = 0
	elif direction == 'right':
		for x in range(height-1, 0, -1):
		    if board[x][width-2] == 2:
		    	check = 0

	

	if check:
		return True
	else:
		return False


def move_block_down():
	#game over check
	for y in range(width):
		if board[3][y] == 3:
			return "game_over"

	#block move procedure
	moved = 0	
	for a in range(height-1, 0, -1):
		for b in range(1, width-1, 1):
			element = board[a][b]
			if element == 2:
				if move_possible_check("down"):
					if not moved:
						for x in range(height-1, 0, -1):
							for y in range(1, width-1, 1):
								if board[x][y] == 2:
									st = "moving x={} y={}".format(a, b)
									#print(st)
									board[x][y] = 1
									board[x+1][y] = 2
						moved = 1
				else:
					for x in range(height-1, 0, -1):
						for y in range(1, width-1, 1):
							if board[x][y] == 2:
								st = "freezing x={} y={}".format(a, b)
								#print(st)
								board[x][y] = 3
					return "block_frozen"

def generate_block():
	r = random.randrange(3)
	r = r + 1
	middle = width / 2
	middle = int(middle)
	global block_position
	if r == 1:
		#square
		board[1][middle] = 2
		board[1][middle + 1] = 2
		board[2][middle] = 2
		board[2][middle + 1] = 2
		return "square"
	elif r == 2:
		#2liner
		board[1][middle] = 2
		board[1][middle+1] = 2
		block_position = "horizontal"
		return "2liner"
		
	elif r == 3:
		#L_block
		board[1][middle] = 2
		board[2][middle] = 2
		board[2][middle+1] = 2
		block_position = "1"
		return "L_block"

def add_frame_to_board():
	for x in range(width):
		board[0][x] = 9
		board[height-1][x] = 9
	for y in range(height):
		board[y][0] = 9
		board[y][width-1] = 9

def print_board():
	for x in range(height):
		for y in range(width):
			element = board[x][y]
			if element == 1:
				print(" ", end = '')
			elif element == 9:
				print(colorama.Fore.GREEN + "#", end = '')
			elif element == 2:
				#print("@", end = '')
				print(colorama.Fore.RED + "@", end = '')
			elif element == 3:
				print(colorama.Fore.BLUE + "O", end = '')
			elif element == 4:
				print(colorama.Fore.CYAN + "O", end = '')
		print("\n", end = '')
	print(score)

add_frame_to_board()
generate_block()
block_generated = 1
#block_position = "horizontal"
#block_type = "2liner"
horizontal_move_direction = ""
kb = KBHit()
block_type = ""
sleep_time = 0.5

while 1:
		#sleep_time = 0.5
		#kb = KBHit()
		if kb.kbhit():
			horizontal_move_direction = kb.getch()
			#if horizontal_move_direction == 'a' or horizontal_move_direction == 'd':
			#	horizontal_control(horizontal_move_direction)
			#elif horizontal_move_direction == 'k':
			#	rotate_block(block_type)
				#print(block_type)
			#elif horizontal_move_direction == 's':
			#	sleep_time = 0.01
			if horizontal_move_direction == 'a':
				if move_possible_check("left"):
					horizontal_control(horizontal_move_direction)
			elif horizontal_move_direction == 'd':
				if move_possible_check("right"):
					horizontal_control(horizontal_move_direction)
			elif horizontal_move_direction == 'k':
				rotate_block(block_type)
			elif horizontal_move_direction == 's':
				sleep_time = 0.01

		if not block_generated:
			block_type = generate_block()
			block_generated = 1
			sleep_time = 0.5
		
		block_shadow("show")
		print_board()
		
		result = move_block_down()
		if result == "game_over":
			break
		elif result == "block_frozen":
			block_generated = 0
			score += score_check()
		
		
		time.sleep(sleep_time)
		block_shadow("hide")
		os.system("clear")

