#lets try to make a maze game
import sys
#below lies array of cells with wall info in 'binary'
#the wall info is a series of boolean values represented as a single int. 
#Each number represents a side and whether or not that side has a wall
#its in order NESW, so a 1010 means there is a wall to the north and south
CellDict = {'1':'1101', '2':'1001','3':'1010','4':'1010','5':'1100','6':'0011','7':'0100','8':'1011','9':'1100','10':'0101','11':'1101','12':'0001','13':'1100','14':'0101','15':'0101','16':'0011','17':'0100','18':'0101','19':'0101','20':'0101','21':'1011','22':'0110','23':'0111','24':'0011','25':'0110'}
#grid layout:
################
#01,02,03,04,05#
#06,07,08,09,10#
#11,12,13,14,15#
#16,17,18,19,20#
#21,22,23,24,25#
################
PlayerPos = 3
PlayerStepCount = 0
def tellWall(CellPos):
	#print("		Start tellWall function")#bug fixing
	if CellPos in CellDict: #sanity check, make sure still in cell grid
		WallInfo = CellDict[CellPos]		#get the info about walls in the new cell
		#print(CellDict[CellPos])#bug fixing
		#print('wall info is ' +WallInfo)#more bug testing
		northWall = int(WallInfo[0:1]) #getting info about each individual wall
		eastWall = int(WallInfo[1:2])
		southWall = int(WallInfo[2:3])#going south is now fixed. did have a bug where if CellDict[CellPos] was an int, ie 1010, going south would make it return a number in the region of 65, instead of the 1010
		westWall = int(WallInfo[3:])
		#print("Wall info looksee " +str(northWall)+str(eastWall)+str(southWall)+str(westWall))#bug fixing
		sumWall = int(northWall)+int(eastWall)+int(southWall)+int(westWall)
		#print("sumwall is " + str(sumWall))#bugtesting
		print("")
		if sumWall == 0:
			print(" There are no walls around this square")
		else:
			if northWall:
				print(" There is a wall to the North")
			if eastWall:
				print(" There is a wall to the East")
			if southWall:
				print(" There is a wall to the South")
			if westWall:
				print(" There is a wall to the West")
		
		#potential ways to say what walls are in new cell:
		#there is a wall to the ____, ____ and ____
		#there is a wall to the ____ and ____
		#there is a wall to the ____
		#there are no walls
	else:
		print("Not in dict, error")
	#print("		End tellWall function")#bug testing
	return
	
def goNewCell(goDirect):
	#print("		Start goNewCell Function")#bug testing
	#single function for all directions, hopefully
	global PlayerPos
	global PlayerStepCount
	playerMoved = False
	WallText = "\n You cannot go that way, there is a wall in the way"
	pos = str(PlayerPos)
	if pos in CellDict:
		if goDirect == 0:
			#north
			if CellDict[pos][goDirect:goDirect+1] == '1': #check to see if north wall is there or not
				print(WallText)
			else:
				print('\n Gone North one square')
				PlayerPos -=5 #move player down one cell in grid
				playerMoved = True
		elif goDirect == 1:
			#east
			if CellDict[pos][goDirect:goDirect+1] == '1': #check to see if east wall is there or not
				print(WallText)
			else:
				print('\n Gone East one square')
				PlayerPos +=1
				playerMoved = True
		elif goDirect == 2:
			#south
			if CellDict[pos][goDirect:goDirect+1] == '1': #check to see if south wall is there or not
				print(WallText)
			else:
				print('\n Gone South one square')
				PlayerPos +=5
				playerMoved = True
		elif goDirect == 3:
			#west
			if CellDict[pos][goDirect:] == '1': #check to see if east wall is there or not
				print(WallText)
			else:
				print('\n Gone West one square')
				PlayerPos -=1
				playerMoved = True
		else:
			print("goDirect not applicable")#only displayed if goDirect somehow not a correct direction (0-3)
		if playerMoved == True: #if the player has moved
			PlayerStepCount +=1
			#print("New location is" +str(PlayerPos))#bug testing
			tellWall(str(PlayerPos));
	#print("		End goNewCell function")#bug testing
	return

def PlayerCommand(Command):#a command to read what the player has typed
	global PlayerPos
	if 'go' in Command:	#if the word go is in the command, they want to move cell, so decide what direction
		if 'north' in Command: #'go north' could be the command
			#print("You want to go north? k")
			goNewCell(0);
		elif 'east' in Command:
			#print("You want to go east? k")
			goNewCell(1);
		elif 'south' in Command:
			#print("You want to go south? k")
			goNewCell(2);
		elif 'west' in Command:
			#print("You want to go west? k")
			goNewCell(3);
		else:
			print("\n I can't tell what direction you want to travel. Please type a compass direction (North, South, East or West)");
	elif "help" in Command:
		print("\n INFORMATION")
		print(" GO ____:  Travel in the typed direction")
		print(" DISTANCE: Displays the total number of squares walked")
		print(" INFO:     Displays information about your current square")
		print(" ClOSE:    Ends the game")
		print(" HELP:     Displays this help text")
		print("           All commands are case insensitive")
	elif "distance" in Command:
		print("\n You have travelled " +str(PlayerStepCount)+ " squares by this point.")
	elif "info" in Command:
		tellWall(str(PlayerPos)); #will repeat what walls are at location using the tellWall function called when the player moves
	elif "close" in Command:
		print("Bye Bye")
		sys.exit()
	#elif 'location' in Command:
		#print(PlayerPos) #used during development for testing and bug finding
	else:
		print("\n " + Command+" is not a recognised command.\n Please type 'help' if you want to know the possible commands")
	return
#start text below! This displays at the beginning of the game
print("\n Welcome to the maze! You find yourself standing just inside\n the start of the maze, having come through the door directly\n north of you, which slammed shut as you entered. In order to\n escape, you'll need to navigate the maze to find the exit!")
print("\n Navigate by typing the command 'Go ____' and the direction you\n wish to travel. Type help if you need help")
tellWall(str(PlayerPos)); # displays wall info for the starter square
while True: # while loop to allow player to keep playing until the end
	PlayerCommand(sys.stdin.readline().strip().lower());
	if PlayerPos == 23: #if player at exit
		break #exit the while loop
		
	
print("\n Congratulations, you found the end!")
print(" It took you " +str(PlayerStepCount)+" squares to find the exit")
raw_input("Hit any key to exit")
