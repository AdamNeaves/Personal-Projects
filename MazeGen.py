#maze generation!
#there is no way this is going to be the most efficient way of doing this
#but it's the only way I can think of at the moment with the knowledge of
#python and general coding that I currently have.

#Credit goes to Tom Doyle for the suggestion of using Prim's Algorithm and
#also lots of help with the generation
import random						#module is needed for the random selection process used in generation

wallLength = int(raw_input('What length would you like the walls? '))						#the length of each wall. This maze generator only generates square mazes, for ease of coding
totalCells = wallLength*wallLength	#total number of cells in the maze
cellMaze= []						#initializing lists for both cells and walls
wallList= []
wallMaze= []						#initializing a list that the generator will use as it generates, adding and subtracting walls
passList= []
cellDict = {}

def genLists():	
	for x in range(1,totalCells): #add all connections between horizontally connected cells
		if x % wallLength !=0: #check to remove illogical connections from cells on the far right wall of the maze
			if x < 9:
				wallList.append('0'+str(x)+',0'+str(x+1)) 	#stored as string so it can be a kind of coordinate
			elif x == 9:									#added zeros to the numbers below ten
				wallList.append('09,10')					#so that all numbers have two digits
			else:
				wallList.append(str(x)+','+str(x+1))
			

	for x in range(1,(totalCells-wallLength)+1): #add all connections between vertically connected cells
		if x+wallLength < 10:									#added zeros to the numbers below
			wallList.append('0'+str(x)+',0'+str(x+wallLength))	#ten so that all digits in the wall
		elif x+wallLength > 9 and x < 10:									#list has two digits
				wallList.append('0'+str(x)+','+str(x+wallLength))
		else:
			wallList.append(str(x)+','+str(x+wallLength)) #added onto the end of the list, so both horizontal and vertical walls are in the same list
	return
#passList is a list of passages, not walls
# Any wall NOT in this list by the end of generation WILL be
#a solid, none passage wall

#right, now that the initial cells and walls have been put into
#lists, the generator itself needs to run

def startGen():
	cellMaze.append('01') #cell one is the one we start in. currently only cell in list
	if wallLength > 9:
		wallMaze.append('01,02')
		wallMaze.append('01,'+str(wallLength+1))	#look at this shitty coding. just look at it
	else:											#it offends my family's honour
		wallMaze.append('01,02')					#adding the walls adjacent to the current cell(s) in the maze
		wallMaze.append('01,0'+str(wallLength+1))	#only cell 01 in the maze (as its the first cell) so only add it's walls
	return
#print('wallList length is: ' +str(len(wallList)))	

def addWalls(selectNum, cellCheck):
	global cellMaze, passList, wallList, wallMaze
	passList.append(wallMaze.pop(selectNum))					#adding wall to passList, marking it as a passage instead of a wall
	#print(selectNum)
	#print('Passage list: ' + str(passList))
	#del wallMaze[selectNum]
	#print('removed wall '+wallMaze[selectNum]+' from the list')
	cellMaze.append(cellCheck)								#adding cell to list of cells in maze
	wallNum = len(wallList)-1
	while wallNum != 0:										#while loop to search the list of walls for potential 
		#print(wallNum)
		#print('Current search: '+ wallList[wallNum])
		if cellCheck in wallList[wallNum]:				#if the new cell number is in the currently searched wall
			wallMaze.append(wallList[wallNum])			#that means it's next to the wall, so add that to potential passages
			wallList.remove(wallList[wallNum])
			#print('Wall Added')
			wallNum = wallNum - 1
		#print(wallMaze)
		if wallNum != 0:							#bit hacky, but a for loop kept crashing for no reason I could see
			wallNum = wallNum - 1					#it works so I didnt question it. BEST PROGRAMMER
	#print('Walls to select are: ' + str(wallMaze))
	#print('Current cells are: ' + str(cellMaze))
	#raw_input('Walls Added')
	return
def genMaze():
	while len(wallMaze) != 0:
		#print("wallMaze length is: " +str(len(wallMaze)))
		select = random.randint(0, len(wallMaze)-1)
		selWall = wallMaze[select]	#search wallMaze for a random wall
		#print('Selected wall is: '+selWall)

		if selWall[3:] in cellMaze:										#if both cells are in cellMaze, remove wall from wallMaze without adding
			if not selWall[0:2] in cellMaze:								#otherwise, one of the cells SHOULD be in cellMaze and
				newCell = selWall[0:2]									#therefore a part of the maze already
				#print('The new cell is: ' + newCell)
				addWalls(select, newCell);
			else:
				#print('Deleting ' + selWall)
				del wallMaze[select]
		elif selWall[0:2] in cellMaze:								#otherwise, one of the cells SHOULD be in cellMaze and
			if not selWall[3:] in cellMaze:
				newCell = selWall[3:]								#therefore a part of the maze already
				#print('The new cell is: ' + newCell)
				addWalls(select, newCell);
			else:
				#print('Deleting ' + selWall)
				del wallMaze[select]
		else:
			print("ERROR, neither cell in maze")			#error catching. hopefully wont see this message when generating, but could if triple digit
															#digit cell numbers get involved due to the search function
	#print('Cells are: ' +str(sorted(cellMaze)))
	#print('Passages are: ')
	#print(str(passList))
	return

def genCellDict():
	global cellMaze, cellDict
	cellMazeSort = sorted(cellMaze)
	for cellNum in range(0,len(cellMazeSort)):			#time to try and convert the info we've generated about passages into something the game can use
		#print(cellNum)
		curCell = cellMazeSort[cellNum]					#variable for the cell we are currently looking at
		#print('Current Cell Is: ' +str(curCell))
		cellPass = "1111"
		for pas in range(0, len(passList)-1):		#search the list of passages for passages containing the current cell
			if curCell in passList[pas]:
				passage = passList[pas]
				#print(passage)
				alphCell = (passage[0:2])			#i was playing fallout 3 at the time shut up
				omegCell = (passage[3:])
				
				if curCell == alphCell:							#this means the current cell is the first cell in the passage, so it is either
					cellDiff = int(omegCell)-int(alphCell)  	#an east or south passage from the current cell
					#print('CellDiff is: ' +str(cellDiff))
					
					if cellDiff == wallLength:					#if the difference between cells is the same as wallLength, it means the passage is south 
						#print('Path is South!')
						cellPass = cellPass[0:2]+'0'+cellPass[3:]
					elif cellDiff == 1:							#if the difference is only 1, it must be an eastern path
						#print('Path is East!')
						cellPass = cellPass[0:1]+'0'+cellPass[2:]
					else:										#if the difference is not 1, or the wallLength, an error has occurred
						print('Difference error!')
						
				elif curCell == omegCell:							#this means the current cell is the second cell in the passage, so it is either
					cellDiff = int(omegCell)-int(alphCell)  	#an east or south passage from the current cell
					#print('CellDiff is: ' +str(cellDiff))
					
					if cellDiff == wallLength:					#if the difference between cells is the same as wallLength, it means the passage is north 
						#print('Path is North!')
						cellPass = '0'+cellPass[1:]
					elif cellDiff == 1:							#if the difference is only 1, it must be an western path
						#print('Path is West!')
						cellPass= cellPass[0:3]+'0'
					else:										#if the difference is not 1, or the wallLength, an error has occurred
						print('Difference error!')												#a north or west passage from the current cell
								
				else:											#if it matches neither, something has gone wrong
					print("Something has gone wrong!")
					print(curCell+ ' is not in ' + passage)
		#print(cellPass)
		cellDict[str(int(curCell))] = cellPass
		print(curCell + " added to dictionary")
	#print('The Cell Dictionary is:')
	#print(cellDict)
	return
	
	
	
