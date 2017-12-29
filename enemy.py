import pygame
import copy
import random

class Enemy(pygame.sprite.Sprite):
	def __init__(self,map,allEnemies,blockWidth,blockHeight,health,numPassed):
		super(Enemy, self).__init__()
		self.map = map
		self.allEnemies = allEnemies
		self.blockWidth = blockWidth
		self.blockHeight = blockHeight
		self.health = health
		self.numPassed = numPassed
	def findRoute(self,map,road):
		route = []
		rows = len(self.map)
		cols = len(self.map[0])
		currentLoc = (0,0)
		lastStep = []
		# find the starting block
		for row in range(rows):
			if self.map[row][0] == 1:
				currentLoc = (row,0)
				route.append(currentLoc)
				break
		# check if the next move is legal
		# the four legal moves
		lane1, lane2 = 1, 2

		# choose random lanes
		if random.randint(1,2) == lane1:
			# go right, go up, go down, and go left
			dirs = [(0,1),(-1,0),(1,0),(0,-1)]
		else:
			# go right, go down, go down, and go left
			dirs = [(0,1),(1,0),(-1,0),(0,-1)]
		if road != []:
			road.pop()
		road.append(dirs[1])
		while currentLoc[1] != cols-1:
			for direction in dirs:
				newRow = currentLoc[0]+direction[0]
				newCol = currentLoc[1]+direction[1]
				if (0<newRow<rows and 0<newCol<cols):
					if (self.map[newRow][newCol] == 1 and (newRow,newCol) not in route):
						currentLoc = (newRow,newCol)
						route.append(currentLoc)
						break
		return route
	def createUnits(self,allEnemies,blockWidth,blockHeight,enemyHealth,path):
		# starting location of the enemies
		# this is where is enemies come out
		locationX = 0
		locationY = int(path[0][0]*self.blockHeight)
		location = (locationX,locationY)
		allEnemies.append(location)

	def oneWave(self,passedEnemies,deadEnemies):
		return len(self.allEnemies)+len(passedEnemies)+len(deadEnemies)

	# move all the units along the path
	def move(self,passedEnemies,enemyHealth,movement,path):
		dx = movement[0]
		dy = movement[1]
		steps = len(path)
		for enemy in self.allEnemies:
			x,y = enemy[0], enemy[1]
			enemyIndex = self.allEnemies.index(enemy)
			currentCell = (enemy[1]//self.blockHeight,enemy[0]//self.blockWidth)
			currentStep = path.index(currentCell)
			if currentStep < steps-1:
				# if move to the right
				if (path[currentStep+1][1] > path[currentStep][1]):
					# prevent from moving out of the box
					if dx == 12:
						currentLoc = (x+dx,y)
						nextCell = (currentLoc[1]//self.blockHeight,
							currentLoc[0]//self.blockWidth)
						if (nextCell in path and path.index(nextCell) == 
							currentStep+1):
							self.allEnemies[enemyIndex] = (x+dx//2, y)
							if nextCell[0] < currentCell[0]:
								self.allEnemies[enemyIndex] = (x, y-dy//2)
							elif nextCell[0] > currentCell[0]:
								self.allEnemies[enemyIndex] = (x, y+dy//2)
						else:
							self.allEnemies[enemyIndex] = (x+dx, y)
					else:
						self.allEnemies[enemyIndex] = (x+dx, y)
				# if move up
				if (path[currentStep+1][0] < path[currentStep][0]):
					self.allEnemies[enemyIndex] = (x, y-dy)
				# if transfrom from up to right
				# get rid of offset
				if (currentStep > 0 and path[currentStep][0] < path[currentStep-1][0] 
					and path[currentStep+1][1] > path[currentStep][1]):
					if (y-dy>=path[currentStep][0]
						*self.blockHeight):
						self.allEnemies[enemyIndex] = (x, y-dy)
				# if move down
				if (path[currentStep+1][0] > path[currentStep][0]):
					self.allEnemies[enemyIndex] = (x, y+dy)
			# the enemies should disappear at the end of the route
			else:
				passed = self.allEnemies.pop(enemyIndex)
				enemyHealth.pop(enemyIndex)
				passedEnemies.append(passed)
				self.numPassed.append(passed)




