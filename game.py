# this is based on the template created by Lukas Peraza for 
# 15-112 S17 Pygame Optional Lecture
# they are from website http://blog.lukasperaza.com/
# all the images are either from google or they are screenshots from
# Three Kingdoms TD

import pygame
import random
import copy
from enemy import Enemy
from soldier import Soldier
from soldier import Swordsman
from soldier import Archer
from soldier import Wizard
from pygamegame import PygameGame

# initialize all the colors
BROWN = (50, 50, 50)
GREEN = (115, 195, 108)
GREEN2 = (50,205,50)
BLUE = (0,0,205)
BLUE2 = (65,105,225)
WHITE = (255,255,255)
LIGHTBLACK = (50, 55, 17)
GRASS = (163,188,75)
RED = (255,30,0)
YELLOW = (255,255,51)

class Game(PygameGame):
	def init(self):
		# self.mode shouldn't be changed
		self.mode = 0
		self.cMode = 0
		self.modes = []
		self.backGround = True
		self.inGame = True
		self.wizardBall = []
		self.archerArrow = []
		self.beatRounds = []
		self.giveStar = 0  
		self.secret = []
		mapVal(self)

	def keyPressed(self, code, mod):
		if code == pygame.K_SPACE:
			self.gameStopped = not self.gameStopped
		if code == pygame.K_UP:
			if self.secret == []:
				self.secret.append("up")
			else:
				self.secret = ["up"]
		if code == pygame.K_DOWN:
			if self.secret == ["up"]:
				self.secret.append("down")
		if code == pygame.K_LEFT:
			if self.secret == ["up","down"]:
				self.secret.append("left")
		if code == pygame.K_RIGHT:
			if self.secret == ["up","down","left"]:
				self.secret.append("right")
		if code == pygame.K_x:
			if self.secret == ["up","down","left","right"]:
				self.secret.append("x")
			if self.secret == ["up","down","left","right","x"]:
				self.secret.append("x")
		if code == pygame.K_l:
			if self.secret == ["up","down","left","right","x","x"]:
				self.secret.append("l")
		if code == pygame.K_r:
			if self.secret == ["up","down","left","right","x","x","l"]:
				self.secret = []
				self.gold = [666]


	def mousePressed(self, x, y):
		self.modes.append(self.mode)
		# if the user clicks the sword
		if (self.mode == 3 and 1 not in self.modes and
			self.swordsLoc[0]<=x<=self.swordsLoc[0]+self.swordSize[0] and
			self.swordsLoc[1]<=y<=self.swordsLoc[1]+self.swordSize[1]):
			# starts the game
			self.mode = 2
			self.cMode = 2
		# clicks to start
		if self.mode == 0:
			self.mode = 3
			self.cMode = 3
			self.modes.append(self.mode)
		# when the user is going to map2
		if (self.mode == 4 and 1 in self.modes):
			if (self.swordsLoc[2]<=x<=self.swordsLoc[2]+self.swordSize[0] and
				self.swordsLoc[3]<=y<=self.swordsLoc[3]+self.swordSize[1]):
				self.mode = 5
				self.cMode = 5
				self.modes.append(self.mode)
		# when the user is going to map3
		if (self.mode == 6 and 1 in self.modes and 4 in self.modes):
			if (self.swordsLoc[4]<=x<=self.swordsLoc[4]+self.swordSize[0] and
				self.swordsLoc[5]<=y<=self.swordsLoc[5]+self.swordSize[1]):
				self.mode = 7
				self.cMode = 7
				self.modes.append(self.mode)
		if self.mode == 2 or self.mode == 1:
			if self.lose == True:
				# if the user loses
				boxWidth, boxHeight = 380, 230
				x1 = (self.width-boxWidth)/2
				y1 = (self.height-boxHeight)/2
				buttonX = boxWidth//3+20
				buttonY = boxHeight//3-20
				# chooses to restart
				if (x1-30<=x<=x1-30+buttonX and 
					y1-50+boxHeight<=y<=y1-50+boxHeight+buttonY):
					if 5 not in self.modes:
						self.modes = []
						self.mode = 1
						mapVal(self)
					elif 7 not in self.modes:
						self.mode = 4
						mapVal(self)
						self.mode = 5
					else:
						self.mode = 7
				x+boxWidth+30-buttonX,y-50+boxHeight
				# chooses to quit
				if (x1+boxWidth+30-buttonX<=x<=x+boxWidth+30 and
					y1-50+boxHeight<=y<=y-50+boxHeight+buttonY):
					self.modes = []
					self.mode = 0 
					self.cMode = 0
					mapVal(self)
			# if the user wins a round
			if self.win == True:
				if 5 not in self.modes:
					self.mode = 4
					self.cMode = 4
					self.beatRounds.append(3)
				elif 7 not in self.modes:
					self.mode = 6
					self.cMode = 6
					self.beatRounds.append(5)
				else:
					self.mode = 0
					self.cMode = 0
					self.modes = []
					mapVal(self)
					self.beatRounds.append(7)

			if (self.menu == False and self.help == False and self.win == False
				and self.lose == False):
				iconSize = 50
				dRatio = 1.8
				# stop/start the game
				if (self.keySpace<=x<=self.keySpace+iconSize and 
					self.keyY<=y<=self.keyY+iconSize):
					self.gameStopped = not self.gameStopped
				# activate the fastforward key
				if (self.keySpace+dRatio*iconSize-10<=x<=
					self.keySpace+(dRatio+1)*iconSize+20 and 
					self.keyY<=y<=self.keyY+iconSize):
					self.fastForward = not self.fastForward
					# when the user chooses to speed up
					if self.fastForward == True:
						self.movement[0] *= 2
						self.movement[1] *= 2
						self.knightMove[0] *= 2
						self.knightMove[1] *= 2
						self.attackSpeed[0] /= 2
						self.attackSpeed[1] /= 2
						self.attackSpeed[2] /= 2
						self.bulletSpeed *= 2
						# make sure the space between stays
						self.movementTime *= 2
					# when chooses to go back
					else:
						self.movement[0] //= 2
						self.movement[1] //= 2
						self.knightMove[0] //= 2
						self.knightMove[1] //= 2
						self.attackSpeed[0] *= 2
						self.attackSpeed[1] *= 2
						self.attackSpeed[2] *= 2
						# make sure the space between stays
						self.movementTime //= 2
						self.bulletSpeed //= 2

				# user clicks on the menu
				if (self.keySpace+2*dRatio*iconSize<=x<=
					self.keySpace+2*dRatio*iconSize+iconSize and
					self.keyY<=y<=self.keyY+iconSize):
					self.menu = True
					effect = pygame.mixer.Sound('images/click.wav')
					effect.play()
				row,col = int(getCell(self, x, y)[0]), int(getCell(self, x, y)[1])
				if self.displayRange == True:
					index = self.allSoldiers.index((self.soldierDisplay[0],
						self.soldierDisplay[1]))

					# allow users to sell the soldiers
					sellX = self.soldierDisplay[1]*self.blockHeight-self.sellSpace
					sellY = self.soldierDisplay[0]*self.blockWidth
					if (sellX<x<sellX+self.blockWidth+10 and sellY<y<sellY+
						self.blockHeight+10):
						self.map[self.soldierDisplay[0]][self.soldierDisplay[1]] = 2
						# return 80 percent of the money when a soldier is sold
						if self.level[index] == 0:
							self.gold.append(int(0.8*self.price[self.soldierTypes[index]]))
						elif self.level[index] == 1:
							self.gold.append(int(0.8*(2*self.price[self.soldierTypes[index]]-20)))
						self.allSoldiers.pop(index)
						self.soldierTypes.pop(index)
						self.level.pop(index)
						sellEffect = pygame.mixer.Sound('images/sell.wav')
						sellEffect.play()
					# allow users to upgrade
					upgradeX = self.soldierDisplay[1]*self.blockHeight+self.sellSpace
					upgradeY = self.soldierDisplay[0]*self.blockWidth
					if (upgradeX<x<upgradeX+self.blockWidth+10 and
						upgradeY<y<upgradeY+self.blockHeight+10 and self.money >=
						int(self.price[self.soldierTypes[index]]-20) and 
						self.level[index] == 0):
						self.gold.append(-int(self.price[self.soldierTypes[index]]-20))
						self.level[index] = 1
						upgradeEffect = pygame.mixer.Sound('images/upgrade.wav')
						upgradeEffect.play()
				self.displayRange = False
				# record the lastclicked row/col
				if self.map[row][col] == 2:
					self.lastClick = []
					self.lastClick.append((row,col))
				elif self.map[row][col] != -1:
					# allow the users to build swordsmen
					if (self.soldierX<x<self.soldierX+self.soldierSizeX and
						self.soldierY<y<self.soldierY+self.soldierSizeY and
						self.lastClick != [] and self.money >= self.price[0]):
						self.gold.append(-self.price[0])
						self.soldierTypes.append(0)
						self.soldierDir.append(1)
						self.level.append(0)
						soldier = Swordsman(self.lastClick[0][0],self.lastClick[0][1],
							self.blockWidth,self.blockHeight,self.attackRange[0],
							self.damage[0],self.gold)
						self.allSoldiers.append(soldier.getPos())
						self.map[soldier.getPos()[0]][soldier.getPos()[1]] = -1
						self.displayRange = True
						self.soldierDisplay = soldier.getPos()
						self.lastClick.pop()
						effect = pygame.mixer.Sound('images/build.wav')
						effect.play()
					# build archers
					if (self.soldierX+self.soldierSizeX+self.soldierSpace<x<
						self.soldierX+2*self.soldierSizeX+self.soldierSpace and
						self.soldierY<y<self.soldierY+self.soldierSizeY and
						self.lastClick != [] and self.money >= self.price[1]):
						self.gold.append(-self.price[1])
						self.soldierTypes.append(1)
						self.soldierDir.append(1)
						self.level.append(0)
						soldier = Archer(self.lastClick[0][0],self.lastClick[0][1],
							self.blockWidth,self.blockHeight,self.attackRange[1],
							self.damage[1],self.gold)
						self.allSoldiers.append(soldier.getPos())
						self.map[soldier.getPos()[0]][soldier.getPos()[1]] = -1
						self.displayRange = True
						self.soldierDisplay = soldier.getPos()
						self.lastClick.pop()
						effect = pygame.mixer.Sound('images/build.wav')
						effect.play()
					# build wizards
					if (self.soldierX+2*self.soldierSizeX+2*self.soldierSpace<x<
						self.soldierX+3*self.soldierSizeX+2*self.soldierSpace and
						self.soldierY<y<self.soldierY+self.soldierSizeY and
						self.lastClick != [] and self.money>= self.price[2]):
						self.gold.append(-self.price[2])
						self.soldierTypes.append(2)
						self.soldierDir.append(1)
						self.level.append(0)
						soldier = Wizard(self.lastClick[0][0],self.lastClick[0][1],
							self.blockWidth,self.blockHeight,self.attackRange[2],
							self.damage[2],self.gold)
						self.allSoldiers.append(soldier.getPos())
						self.map[soldier.getPos()[0]][soldier.getPos()[1]] = -1
						self.displayRange = True
						self.soldierDisplay = soldier.getPos()
						self.lastClick.pop()
						effect = pygame.mixer.Sound('images/build.wav')
						effect.play()
					elif self.lastClick != []:
						self.lastClick.pop()
				# allows the user to see the attack range
				elif self.map[row][col] == -1:
					row, col = getCell(self,x,y)[0], getCell(self,x,y)[1]
					self.displayRange = True
					# allow the soldiers to ask quesitons
					# eg. shenme, wei?
					decider = random.randint(1,3)
					if decider == 1:
						effect = pygame.mixer.Sound('images/q1.wav')
					elif decider == 2:
						effect = pygame.mixer.Sound('images/q2.wav')
					else:
						effect = pygame.mixer.Sound('images/q3.wav')
					effect.play()
					self.soldierDisplay = (row,col)
			elif self.help == False and self.win == False and self.lose == False:
				barWidth = 183
				barHeight = 55
				# user chooses to resume the game
				if ((self.width-barWidth)/2<=x<=(self.width+barWidth)/2 and 
					(self.height-barHeight)/2-105<=y<=
					(self.height-barHeight)/2-105+barHeight):
					self.menu = False
					self.gameStopped = False
					effect = pygame.mixer.Sound('images/click.wav')
					effect.play()
				# user chooses to restart
				elif ((self.width-barWidth)/2<=x<=(self.width+barWidth)/2 and 
					(self.height-barHeight)/2-35<=y<=
					(self.height-barHeight)/2-35+barHeight):
					effect = pygame.mixer.Sound('images/click.wav')
					effect.play()
					if 5 not in self.modes or self.cMode == 2:
						#self.modes = []
						self.mode = 2
						mapVal(self)
					elif 7 not in self.modes or self.cMode == 5:
						self.mode = 4
						mapVal(self)
						self.mode = 5
					else:
						self.mode = 6
						mapVal(self)
						self.mode = 7
				# user clicks for help
				elif ((self.width-barWidth)/2<=x<=(self.width+barWidth)/2 and 
					(self.height-barHeight)/2+35<=y<=
					(self.height-barHeight)/2+35+barHeight):
					self.help = True
					effect = pygame.mixer.Sound('images/click.wav')
					effect.play()
				# the user chooses to quit the game
				elif ((self.width-barWidth)/2<=x<=(self.width+barWidth)/2 and 
					(self.height-barHeight)/2+105<=y<=
					(self.height-barHeight)/2+105+barHeight):
					effect = pygame.mixer.Sound('images/click.wav')
					effect.play()
					if 4 not in self.modes and len(self.modes) > 2:
						self.modes = []
						self.mode = 3
						self.cMode = 3
						mapVal(self)
					elif 6 not in self.modes and len(self.modes) > 2:
						self.mode = 4
						self.cMode = 4
					else:
						self.mode = 6
						self.cMode = 6
			# user clicks for help
			elif self.help == True:
				width = 696
				height = 456
				iconSize = 50
				# close the help window
				if ((self.width-width)/2+15<=x<=(self.width-width)/2+30 and
					(self.height-height)/2+15<=y<=(self.height-height)/2+30):
					self.help = False
					self.page = 0
					effect = pygame.mixer.Sound('images/click.wav')
					effect.play()
				# clicks on the right arrow
				elif ((self.width+width)/2-iconSize-30<=x<=(self.width+width)/2-30
					and ((self.height+height)/2-iconSize-20<=y<=
					(self.height+height)/2) and self.page < self.pages):
					self.page += 1
					effect = pygame.mixer.Sound('images/wizardShoot.wav')
					effect.play()
				# clicks on the left arrow
				elif ((self.width-width)/2+30<=x<=(self.width-width)/2+30+iconSize
					and (self.height+height)/2-iconSize-20<=y<=
					(self.height+height)/2-20 and self.page > 0):
					self.page -= 1
					effect = pygame.mixer.Sound('images/wizardShoot.wav')
					effect.play()
		# if the user advances to the second map
		if self.mode == 5:
			mapVal(self)
		if self.mode == 7:
			mapVal(self)

		# if the user is looking at the game background
		if (self.modes != [] and len(self.modes) < 2 and self.mode == 3 or 
			self.mode == 4 or self.mode == 6):
			# allow users to go back to a map that is already beaten
			if 3 in self.beatRounds:
				# allow the user to click the first castle to go back
				if 230 < x < 330 and 20 < y < 130:
					self.mode = 2
					self.cMode = 2
					mapVal(self)
			if 5 in self.beatRounds:
				if 470 < x < 590 and 50 < y < 170:
					self.mode = 5
					self.cMode = 5
					mapVal(self)
			if 7 in self.beatRounds:
				if 340 < x < 500 and 250 < y < 400:
					self.mode = 7
					self.cMode = 7
					mapVal(self)


	def timerFired(self, dt):
		# make the wizard balls to move
		self.wizardBall2 = copy.deepcopy(self.wizardBall)
		count = 0
		for i in range(len(self.wizardBall2)):
			realX = int(self.wizardBall[i-count][2]+(self.blockWidth-10))
			realY = int(self.wizardBall[i-count][3]+(self.blockWidth-10)/2)
			# find the ratio and figure out how much the ball moves in 
			# x and y direction
			if (realX - self.wizardBall[i-count][0]) != 0:
				xPortion = abs(realX - self.wizardBall[i-count][0])/(abs(realX - 
					self.wizardBall[i-count][0]) + abs(realY - self.wizardBall[i-count][1]))
			else:
				xPortion = 0
			yPortion = 1 - xPortion
			if self.soldierDir[self.wizardBall[i-count][4]] == -1:
				self.wizardBall[i-count][0] -= xPortion*self.bulletSpeed
			else:
				self.wizardBall[i-count][0] += xPortion*self.bulletSpeed
			if (realY - self.wizardBall[i-count][1]) >= 0:
				self.wizardBall[i-count][1] += yPortion*self.bulletSpeed
			else:
				self.wizardBall[i-count][1] -= yPortion*self.bulletSpeed
			if abs(realX - self.wizardBall[i-count][0]) < self.bulletSpeed/2:
				self.wizardBall.pop(i-count)
				count += 1
			elif abs(realY - self.wizardBall[i-count][1]) < self.bulletSpeed/2:
				self.wizardBall.pop(i-count)
				count += 1

		# make the archer arrows to move
		self.archerArrow2 = copy.deepcopy(self.archerArrow)
		count = 0
		for i in range(len(self.archerArrow2)):
			realX = int(self.archerArrow[i-count][2]+(self.blockWidth-10))
			realY = int(self.archerArrow[i-count][3]+(self.blockWidth-10)/2)
			# find the ratio and figure out how much the ball moves in 
			# x and y direction
			if (realX - self.archerArrow[i-count][0]) != 0:
				xPortion = abs(realX - self.archerArrow[i-count][0])/(abs(realX - 
					self.archerArrow[i-count][0]) + abs(realY - self.archerArrow[i-count][1]))
			else:
				xPortion = 0
			yPortion = 1 - xPortion
			if self.soldierDir[self.archerArrow[i-count][4]] == -1:
				self.archerArrow[i-count][0] -= xPortion*self.bulletSpeed
			else:
				self.archerArrow[i-count][0] += xPortion*self.bulletSpeed
			if (realY - self.archerArrow[i-count][1]) >= 0:
				self.archerArrow[i-count][1] += yPortion*self.bulletSpeed
			else:
				self.archerArrow[i-count][1] -= yPortion*self.bulletSpeed
			if abs(realX - self.archerArrow[i-count][0]) < self.bulletSpeed/2:
				self.archerArrow.pop(i-count)
				count += 1
			elif abs(realY - self.archerArrow[i-count][1]) < self.bulletSpeed/2:
				self.archerArrow.pop(i-count)
				count += 1






		# get the background music
		if self.mode == 1 or self.mode == 2 or self.mode == 5 or self.mode == 7:
			if self.inGame == True:
				self.inGame = False
				pygame.mixer.music.load('images/inGame1.mp3')
				pygame.mixer.music.play(-1)
				self.backGround = True
		elif self.backGround == True:
			self.backGround = False
			pygame.mixer.music.load('images/backGround2.mp3')
			pygame.mixer.music.play(-1)
			self.inGame = True

		# swords floating
		if self.mode == 3:
			self.swordsLoc[1] += 2*self.swordsDir
			if (self.swordsLoc[1] >= self.swordsPos[0][1]+10 or 
				self.swordsLoc[1] <= self.swordsPos[0][1]-10):
				self.swordsDir = -self.swordsDir
		if self.mode == 4:
			self.swordsLoc[3] += 2*self.swordsDir
			if (self.swordsLoc[3] >= self.swordsPos[1][1]+10 or 
				self.swordsLoc[3] <= self.swordsPos[1][1]-10):
				self.swordsDir = -self.swordsDir
		if self.mode == 6:
			self.swordsLoc[5] += 2*self.swordsDir
			if (self.swordsLoc[5] >= self.swordsPos[2][1]+10 or 
				self.swordsLoc[5] <= self.swordsPos[2][1]-10):
				self.swordsDir = -self.swordsDir
		if self.win or self.lose:
			self.gameStopped = True
		# making the initial clickng hint
		self.clickSize += 3*self.clickDir
		if (self.clickSize >= 55 or self.clickSize <= 45):
			self.clickDir = -self.clickDir
		# user clicks menu
		if self.menu == True:
			self.gameStopped = True
		if self.mode == 2 or self.mode == 1 or self.mode == 5 or self.mode == 7:
			self.mode = 1
			self.money = sum(self.gold)
			# losing the game
			self.lives = 10 - len(self.passedEnemies)
			if self.lives <= 0:
				self.gameOver = True
				self.lose = True
			# winning the game
			if self.waves == [] and self.lose == False:
				self.gameOver = True
				self.win = True
			if self.gameOver:
				self.gameStopped = True
			# count time
			if self.gameStopped == False:
				self.time += self.movementTime
				self.ghostTime += 1
				self.attackingTime += 1
				self.attackTime0 += 1
				self.attackTime1 += 1
				self.attackTime2 += 1

				# show waves
				if 0 < self.time < 10:
					self.showWave = True

				# used for the space between enemies
				if self.time > 20:
					self.showWave = False
					# wizards attacking
					if self.waves[0][1] == 0:
						enemy = Enemy(self.map,self.allEnemies,self.blockWidth,
							self.blockHeight,self.health[0],self.numPassed)
						enemy.createUnits(self.allEnemies,
							self.cellWidth,self.cellHeight,self.enemyHealth,self.path)
						self.enemyHealth.append(self.health[0])
						self.time -= self.spaceTime
					# archers attacking
					elif self.waves[0][1] == 1:
						enemy = Enemy(self.map,self.allEnemies,self.blockWidth,
							self.blockHeight,self.health[1],self.numPassed)
						enemy.createUnits(self.allEnemies,
							self.cellWidth,self.cellHeight,self.enemyHealth,self.path)
						self.enemyHealth.append(self.health[1])
						self.time -= self.spaceTime
					# knights attacking
					elif self.waves[0][1] == 2:
						enemy = Enemy(self.map,self.allEnemies,self.blockWidth,
							self.blockHeight,self.health[2],self.numPassed)
						enemy.createUnits(self.allEnemies,
							self.cellWidth,self.cellHeight,self.enemyHealth,self.path)
						self.enemyHealth.append(self.health[2])
						# they are on horses, so they can move closer to 
						# each other
						self.time -= 0.6*self.spaceTime
					self.createdUnits += 1
					if self.waves != []:
						if self.waves[0][0] == self.createdUnits:
							self.time = -1000

				# used for generating the ghost image
				if self.ghostTime > 20:
					self.hint = False
					if self.justDied != []:
						self.justDied.pop()
						self.ghostTime -= 1
						killed = pygame.mixer.Sound('images/killed.wav')
						killed.play()

				# used for generating attacking animation
				if self.attackingTime > 20:
					if self.attacking != []:
						self.attacking = []
						self.attackingTime -= 0.5

				# move the enemies along the path
				if self.waves[0][1] == 0:
					Enemy(self.map,self.allEnemies,self.blockWidth,
						self.blockHeight,self.health[0],self.numPassed).move(
						self.passedEnemies,self.enemyHealth,self.movement,self.path)
				elif self.waves[0][1] == 1:
					Enemy(self.map,self.allEnemies,self.blockWidth,
						self.blockHeight,self.health[1],self.numPassed).move(
						self.passedEnemies,self.enemyHealth,self.movement,self.path)
				elif self.waves[0][1] == 2:
					Enemy(self.map,self.allEnemies,self.blockWidth,
						self.blockHeight,self.health[2],self.numPassed).move(
						self.passedEnemies,self.enemyHealth,self.knightMove,self.path)

				# used for swordsman's attack speed
				if self.attackTime0 > 20:
					for soldier in self.allSoldiers:
						index = self.allSoldiers.index(soldier)
						if self.soldierTypes[index] == 0:
							soldiers = Swordsman(soldier[0],soldier[1],self.blockWidth,
								self.blockHeight,self.attackRange[0],self.damage[0],
								self.gold)
							soldiers.attack(self.allEnemies,self.justDied,
								self.enemyHealth,self.deadEnemies,self.level,
								self.soldierTypes,self.allSoldiers,self.attacking,
								self.soldierDir,self.wizardBall,self.archerArrow)
					self.attackTime0 -= self.attackSpeed[0]
				# used for archer's attack speed
				if self.attackTime1 > 20:
					for soldier in self.allSoldiers:
						index = self.allSoldiers.index(soldier)
						if self.soldierTypes[index] == 1:
							soldiers = Archer(soldier[0],soldier[1],self.blockWidth,
								self.blockHeight,self.attackRange[1],self.damage[1],
								self.gold)
							soldiers.attack(self.allEnemies,self.justDied,
								self.enemyHealth,self.deadEnemies,self.level,
								self.soldierTypes,self.allSoldiers,self.attacking,
								self.soldierDir,self.wizardBall,self.archerArrow)
					self.attackTime1 -= self.attackSpeed[1]

				# used for wizard's attack speed
				if self.attackTime2 > 20:
					for soldier in self.allSoldiers:
						index = self.allSoldiers.index(soldier)
						if self.soldierTypes[index] == 2:
							soldiers = Wizard(soldier[0],soldier[1],self.blockWidth,
								self.blockHeight,self.attackRange[2],self.damage[2],
								self.gold)
							soldiers.attack(self.allEnemies,self.justDied,
								self.enemyHealth,self.deadEnemies,self.level,
								self.soldierTypes,self.allSoldiers,self.attacking,
								self.soldierDir,self.wizardBall,self.archerArrow)
					self.attackTime2 -= self.attackSpeed[2]	

				# disperse the next wave
				totalDistroyed = len(self.deadEnemies)+len(self.numPassed)
				if self.time < -10 and totalDistroyed == self.waves[0][0]:
					self.createdUnits = 0
					self.deadEnemies = []
					self.numPassed = []
					self.waves.pop(0)
					# gold increases by 50 everywaves win
					self.gold.append(50)
					self.time = -10
					# make the next wave choose a random path
					self.path = Enemy(self.map,self.allEnemies,
						self.blockWidth,self.blockHeight,self.health,
						self.numPassed).findRoute(self.map,self.random)



	def redrawAll(self, screen):
		if self.mode == 0:
			displayInitialScreen(self,screen)
		elif self.mode == 3 or self.mode == 4 or self.mode == 6:
			drawBackground(self,screen)
			drawWinStars(self,screen)
		elif self.mode == 1:
			drawMap(self, screen)
			drawIcons(self, screen)
			drawSelected(self, screen)
			drawSoldiers(self,screen)
			drawEnemies(self,screen)
			drawRange(self,screen)
			drawSoul(self,screen)
			drawCastle(self,screen)
			drawWaves(self,screen)
			drawMenu(self,screen)
			drawHelp(self,screen)
			drawGame(self,screen)
			drawComingDir(self,screen)
			drawAttackObject(self,screen)

def getCell(self, x, y):
	row = y//self.cellHeight
	col = x//self.cellWidth
	return (row,col)

def soldierType(self):
	self.level = []
	self.damage = [28,17,13]
	self.movement = [6,6]
	self.knightMove = [8,8]
	self.attackSpeed = [6,4,4]
	self.soldierTypes = []
	self.soldierDir = []
	self.attackRange = [80,120,140]
	self.boostedRange = [100,140,160]

def mapVal(self):
	soldierType(self)
	self.bulletSpeed = 30
	# tells the user where the enemies will go
	self.random = []
	self.waves = [(5,0),(8,0),(8,1),(5,2),(12,1),(15,2),(20,2)]
	# different map has different wave
	if self.mode == 5:
		self.waves = [(10,0),(10,1),(15,1),(8,2),(20,2)]
	elif self.mode == 7:
		self.waves = [(8,0),(7,1),(12,0),(12,1),(5,2),(15,1),(12,2),(20,2),(30,2)]
	self.totalWaves = len(self.waves)
	self.gold = [360]
	if self.mode == 7:
		self.gold = [600]
	self.price = [80,90,100]
	self.showWave = False
	self.menu = False
	self.help = False
	self.hint = True
	self.pages = 4
	self.page = 0
	self.fastForward = False
	self.gameStopped = False
	self.win = False
	self.lose = False
	self.displayRange = False
	self.soldierDisplay = None
	self.time = 0
	self.movementTime = 1
	self.ghostTime = 0
	self.attackTime0 = 0
	self.attackTime1 = 0
	self.attackTime2 = 0
	self.attackingTime = 0
	self.spaceTime = 10
	self.gameOver = False
	self.keyY = self.height - 60
	self.keyY2 = 30
	self.keySpace = 30
	self.soldierSpace = 15
	self.sellSpace = 70
	self.soldierY = self.height - 110
	self.soldierX = self.width - 300
	self.lastClick = []
	self.allSoldiers = []
	self.allEnemies = []
	self.enemyHealth = []
	self.deadEnemies = []
	self.justDied = []
	self.attacking = []
	self.passedEnemies = []
	self.createdUnits = 0
	self.numPassed = []
	self.health = [170,260,350]
	if self.mode == 5:
		self.health = [270,420,630]
	elif self.mode == 7:
		self.health = [210,350,500]
	self.soldierSizeX, self.soldierSizeY = 80, 100
	self.swordsPos = [(280,40),(520,70),(400,300)]
	self.swordsLoc = [280,40,520,70,400,300]
	self.swordsDir = 1
	self.clickSize = 50
	self.clickDir = 1
	self.rows, self.cols = 15, 15
	self.map = [([0] * self.cols) for row in range(self.rows)]
	self.blockWidth = self.width//self.cols
	self.blockHeight = self.height//self.rows
	self.cellWidth = self.width//self.cols
	self.cellHeight = self.height//self.rows
	self.castle = None
	startRow = 11
	turnCol1 = self.cols//2
	# make map1
	for i in range(turnCol1):
		self.map[startRow][i] = 1
	turnRow1 = 3
	for i in range(turnRow1, startRow+1):
		self.map[i][turnCol1] = 1
	for i in range(turnCol1, self.cols):
		self.map[turnRow1][i] = 1
	# tell the users when they can put soldiers
	directions = [(-1,-1),(-1,0),(-1,1),
			(0,-1),		  (0,1),
			(1,-1),(1,0),(1,1)]
	for row in range(self.rows):
		for col in range(self.cols):
			for direction in directions:
				if (0<row+direction[0]<15 and 0<col+direction[1]<15):
					if (self.map[row][col] != 1 and 
						self.map[row+direction[0]][col+direction[1]] == 1):
						self.map[row][col] = 2
	if self.mode != 7:
		# make the castle at the end of the path
		for row in range(self.rows):
			if self.map[row][self.cols-1] == 2:
				self.map[row][self.cols-1] = 3
				self.castle = (row,self.cols-1)
				break
		for row in range(self.rows):
			if self.map[row][self.cols-1] == 2:
				self.map[row][self.cols-1] = 4
	elif self.mode == 7:
		self.map[7][14] = 3
		self.castle = (6,14)
		self.map[6][14] = 4
		self.map[8][14] = 4

	# map2
	if self.mode == 5:
		for row in range(self.rows):
			for col in range(self.cols):
				self.map[row][col] = 0
		self.map[12][0] = 1
		for i in range(12,1,-1):
			self.map[i][1] = 1
		for i in range(1,4):
			self.map[2][i] = 1
		for i in range(2,13):
			self.map[i][3] = 1
		self.map[12][4] = 1
		self.map[12][5] = 1
		for i in range(12,1,-1):
			self.map[i][5] = 1
		self.map[2][6] = 1
		self.map[2][7] = 1
		for i in range(2,13):
			self.map[i][7] = 1
		self.map[12][8] = 1
		self.map[12][9] = 1
		for i in range(12,1,-1):
			self.map[i][9] = 1
		self.map[2][10] = 1
		self.map[2][11] = 1
		for i in range(2,13):
			self.map[i][11] = 1
		self.map[12][12] = 1
		for i in range(12,2,-1):
			self.map[i][13] = 1
		self.map[3][14] = 1
		# tell the user where to put soldiers
		for i in range(3,13):
			self.map[i][2] = 2
		for i in range(2,12):
			self.map[i][4] = 2
		for i in range(3,13):
			self.map[i][6] = 2
		for i in range(2,12):
			self.map[i][8] = 2
		for i in range(3,13):
			self.map[i][10] = 2
		for i in range(3,12):
			self.map[i][12] = 2

	# map3
	if self.mode == 7:
		for row in range(self.rows):
			for col in range(self.cols):
				self.map[row][col] = 0
		#for col in range(self.cols):
		#	self.map[7][col] = 1
		for col in range(3):
			self.map[7][col] = 1
		for row in range(2,13):
			self.map[row][2] = 1
		for col in range(2,13):
			self.map[2][col] = 1
			self.map[12][col] = 1
		for row in range(2,13):
			self.map[row][12] = 1
		self.map[7][13] = 1
		self.map[7][14] = 1
		self.map[6][1] = 2
		self.map[6][3] = 2
		self.map[6][11] = 2
		self.map[7][3] = 2
		self.map[7][11] = 2
		self.map[8][1] = 2
		self.map[8][3] = 2
		self.map[8][11] = 2
		self.map[3][3] = 2
		self.map[3][4] = 2
		self.map[4][3] = 2
		self.map[10][3] = 2
		self.map[11][3] = 2
		self.map[11][4] = 2
		self.map[5][11] = 2
		self.map[9][11] = 2
		self.map[10][11] = 2
		self.map[11][11] = 2
		self.map[4][11] = 2
		self.map[3][11] = 2
		self.map[3][10] = 2
		self.map[11][10] = 2
		self.map[5][3] = 2
		self.map[9][3] = 2
		self.map[5][1] = 2
		self.map[9][1] = 2
		

	# initialize the path for enemies
	self.path = Enemy(self.map,self.allEnemies,self.blockWidth,
		self.blockHeight,self.health,self.numPassed).findRoute(self.map,
		self.random)
	self.swordSize = (self.blockWidth-20,self.blockHeight+20)

# draw the fireball or arrows shot out by archers/wizards
def drawAttackObject(self,screen):
	wizardBall = pygame.transform.scale(pygame.image.load
		("images/wizardBall.png").convert_alpha(),(15,15))
	arrowL1 = pygame.transform.scale(pygame.image.load
		("images/arrowL1.png").convert_alpha(),(22,22))
	arrowL2 = pygame.transform.scale(pygame.image.load
		("images/arrowL2.png").convert_alpha(),(25,15))
	arrowL3 = pygame.transform.scale(pygame.image.load
		("images/arrowL3.png").convert_alpha(),(18,25))
	arrowR1 = pygame.transform.scale(pygame.image.load
		("images/arrowR1.png").convert_alpha(),(20,23))
	arrowR2 = pygame.transform.scale(pygame.image.load
		("images/arrowR2.png").convert_alpha(),(25,15))
	arrowR3 = pygame.transform.scale(pygame.image.load
		("images/arrowR3.png").convert_alpha(),(18,25))
	theArrow = pygame.transform.scale(pygame.image.load
		("images/theArrow.png").convert_alpha(),(27,12))
	for i in range(len(self.wizardBall)):
		# draw wizard balls
		screen.blit(wizardBall,(self.wizardBall[i][0],self.wizardBall[i][1]))
	# draw the arrows
	for i in range(len(self.archerArrow)):
		arrow = pygame.transform.rotate(theArrow,self.archerArrow[i][5])
		screen.blit(arrow,(self.archerArrow[i][0],self.archerArrow[i][1]))


def drawWinStars(self,screen):
	star = pygame.transform.scale(pygame.image.load
		("images/star.png").convert_alpha(),(25,25))
	if 3 in self.beatRounds:
		# draw stars on the map after winning
		if self.giveStar > 0:
			screen.blit(star,(265,45),area=None)
		if self.giveStar > 1:
			screen.blit(star,(290,32),area=None)
		if self.giveStar > 2:
			screen.blit(star,(315,45),area=None)
	if 5 in self.beatRounds:
		if self.giveStar > 0:
			screen.blit(star,(505,75),area=None)
		if self.giveStar > 1:
			screen.blit(star,(530,62),area=None)
		if self.giveStar > 2:
			screen.blit(star,(555,75),area=None)
	if 7 in self.beatRounds:
		if self.giveStar > 0:
			screen.blit(star,(375,295),area=None)
		if self.giveStar > 1:
			screen.blit(star,(400,282),area=None)
		if self.giveStar > 2:
			screen.blit(star,(425,295),area=None)

# draw the map of different villages
def drawBackground(self,screen):
	initialScreen = pygame.transform.scale(pygame.image.load
		("images/map.png").convert_alpha(),(self.width,self.height))
	screen.blit(initialScreen,(0,0),area=None)
	if self.mode == 3:
		sword = pygame.transform.scale(pygame.image.load
			("images/current.png").convert_alpha(),(self.swordSize[0],
			self.swordSize[1]))
		screen.blit(sword,(self.swordsLoc[0],self.swordsLoc[1]))
	elif self.mode == 4:
		sword = pygame.transform.scale(pygame.image.load
			("images/current.png").convert_alpha(),(self.swordSize[0],
			self.swordSize[1]))
		screen.blit(sword,(self.swordsLoc[2],self.swordsLoc[3]))
	elif self.mode == 6:
		sword = pygame.transform.scale(pygame.image.load
			("images/current.png").convert_alpha(),(self.swordSize[0],
			self.swordSize[1]))
		screen.blit(sword,(self.swordsLoc[4],self.swordsLoc[5]))

# tell the user which way the soldiers are coming
def drawComingDir(self,screen):
	if self.health == [210,350,500] and self.showWave == True:
		dirArrow1 = pygame.transform.scale(pygame.image.load
			("images/dirArrow1.png").convert_alpha(),(50,50))
		dirArrow2 = pygame.transform.scale(pygame.image.load
			("images/dirArrow2.png").convert_alpha(),(50,50))
		if self.random[0] == (-1,0):
			screen.blit(dirArrow2,(360,180))
		else:
			screen.blit(dirArrow1,(360,720))


		

def drawHelp(self,screen):
	iconSize = 50
	if self.help == True:
		width = 696
		height = 456
		helpScreen = pygame.transform.scale(pygame.image.load
			("images/box.jpeg").convert_alpha(),(width,height))
		screen.blit(helpScreen,((self.width-width)/2,(self.height-height)/2),
			area=None)
		close = pygame.transform.scale(pygame.image.load
			("images/close.png").convert_alpha(),(15,15))
		screen.blit(close,((self.width-width)/2+15,(self.height-height)/2+15),area=None)
		# the right arrow
		if self.page != self.pages:
			right = pygame.transform.scale(pygame.image.load
				("images/right.png").convert_alpha(),(iconSize,iconSize))
			screen.blit(right,((self.width+width)/2-iconSize-30,
				(self.height+height)/2-iconSize-20),area=None)
		# the left arrow
		if self.page != 0:
			left = pygame.transform.scale(pygame.image.load
				("images/left.png").convert_alpha(),(iconSize,iconSize))
			screen.blit(left,((self.width-width)/2+30,
				(self.height+height)/2-iconSize-20),area=None)
		# the 0th page
		if self.page == 0:
			demoWidth = int(0.7*width)
			demoHeight = int(0.7*height)
			demo1 = pygame.transform.scale(pygame.image.load
				("images/demo1.png").convert_alpha(),(demoWidth,demoHeight))
			screen.blit(demo1,((self.width-demoWidth)/2,
				(self.height-demoHeight)/2),area=None)
		# the first page
		if self.page == 1:
			demoWidth = int(0.55*width)
			demoHeight = int(0.55*height)
			wordWidth = 594
			wordHeight = 60
			demo2 = pygame.transform.scale(pygame.image.load
				("images/demo2.png").convert_alpha(),(demoWidth,demoHeight))
			screen.blit(demo2,((self.width-demoWidth)/2,
				(self.height-demoHeight)/2-50),area=None)
			word1 = pygame.transform.scale(pygame.image.load
				("images/word1.png").convert_alpha(),(wordWidth,wordHeight))
			screen.blit(word1,((self.width-wordWidth)/2,
				(self.height-demoHeight)/2-50+demoHeight),area=None)
		introWidth = 540
		introHeight = 130
		# the second page
		if self.page == 2:
			intro1 = pygame.transform.scale(pygame.image.load
				("images/intro1.png").convert_alpha(),(introWidth,introHeight))
			screen.blit(intro1,((self.width-introWidth)/2,
				(self.height-introHeight)/2-100),area=None)
			intro2 = pygame.transform.scale(pygame.image.load
				("images/intro2.png").convert_alpha(),(introWidth,introHeight))
			screen.blit(intro2,((self.width-introWidth)/2,
				(self.height-introHeight)/2+50),area=None)
		# the third page
		if self.page == 3:
			intro3 = pygame.transform.scale(pygame.image.load
				("images/intro3.png").convert_alpha(),(introWidth,introHeight))
			screen.blit(intro3,((self.width-introWidth)/2,
				(self.height-introHeight)/2-100),area=None)
			intro4 = pygame.transform.scale(pygame.image.load
				("images/intro4.png").convert_alpha(),(introWidth,introHeight))
			screen.blit(intro4,((self.width-introWidth)/2,
				(self.height-introHeight)/2+50),area=None)
		# the final page
		if self.page == 4:
			intro5 = pygame.transform.scale(pygame.image.load
				("images/intro5.png").convert_alpha(),(introWidth,introHeight))
			screen.blit(intro5,((self.width-introWidth)/2,
				(self.height-introHeight)/2-100),area=None)
			intro6 = pygame.transform.scale(pygame.image.load
				("images/intro6.png").convert_alpha(),(introWidth,introHeight))
			screen.blit(intro6,((self.width-introWidth)/2,
				(self.height-introHeight)/2+50),area=None)
		
def drawMenu(self,screen):
	if self.menu == True:
		width = 260
		height = 352
		barWidth = 183
		barHeight = 55
		menu = pygame.transform.scale(pygame.image.load
			("images/menu.png").convert_alpha(),(width,height))
		screen.blit(menu,((self.width-width)/2,(self.height-height)/2),area=None)
		helpBar = pygame.transform.scale(pygame.image.load
			("images/help.png").convert_alpha(),(barWidth,barHeight))
		screen.blit(helpBar,((self.width-barWidth)/2,
			(self.height-barHeight)/2+35),area=None)

# the cover image
def displayInitialScreen(self,screen):
	initialScreen = pygame.transform.scale(pygame.image.load
		("images/threeKingdoms.png").convert_alpha(),(self.width,self.height))
	screen.blit(initialScreen,(0,0),area=None)
	myfont = pygame.font.SysFont("arial", self.blockHeight+20)
	toContinue = myfont.render("Click to Continue", 1, WHITE)
	screen.blit(toContinue, (self.width//2-3*(self.blockHeight+20),
		self.keyY-self.blockHeight+20))

def drawGame(self,screen):
	boxWidth, boxHeight = 380, 230
	x = (self.width-boxWidth)/2
	y = (self.height-boxHeight)/2
	buttonX = boxWidth//3+20
	buttonY = boxHeight//3-20
	gameOver = 	pygame.transform.scale(pygame.image.load
		("images/gameOver.png").convert_alpha(),(boxWidth,boxHeight))
	restart = pygame.transform.scale(pygame.image.load
		("images/restart.png").convert_alpha(),(buttonX,buttonY))
	quit = pygame.transform.scale(pygame.image.load
		("images/quit.png").convert_alpha(),(buttonX,buttonY))
	win = pygame.transform.scale(pygame.image.load
		("images/win.png").convert_alpha(),(self.width,self.height))
	if self.lose == True:
		screen.blit(gameOver,(x,y-50),area = None)
		screen.blit(restart,(x-30,y-50+boxHeight),area=None)
		# I drew the graph and the x coordinate turns out to be
		# x+boxWidth+30-buttonX
		screen.blit(quit,(x+boxWidth+30-buttonX,y-50+boxHeight),area=None)
	elif self.win == True:
		if self.lives >= 9:
			self.giveStar = 3
		elif self.lives >= 5:
			self.giveStar = 2
		else:
			self.giveStar = 1
		screen.blit(win,(0,0),area = None)
		myfont = pygame.font.SysFont("arial", self.blockHeight+20)
		toContinue = myfont.render("Click to Continue", 1, WHITE)
		screen.blit(toContinue, (self.width//2-3*(self.blockHeight+20),
			self.keyY-self.blockHeight+20))

def drawWaves(self,screen):
	if self.showWave == True:
		drawBox(self,screen)
		drawEnemyWaves(self,screen)
		drawNumEnemies(self,screen)

def drawBox(self,screen):
	boxWidth, boxHeight = 380, 230
	x = (self.width-boxWidth)/2
	y = (self.height-boxHeight)/2
	pygame.draw.rect(screen,LIGHTBLACK,(x,y,boxWidth,boxHeight))

def drawEnemyWaves(self,screen):
	x = (self.width-self.blockWidth)/2
	y = (self.height-self.blockHeight)/2-50
	if self.waves[0][1] == 0:
		waves = pygame.transform.scale(pygame.image.load
			("images/wave0.png").convert_alpha(),(self.blockWidth,
			self.blockHeight+10))
		screen.blit(waves,(x,y),area = None)
	elif self.waves[0][1] == 1:
		waves = pygame.transform.scale(pygame.image.load
			("images/wave1.png").convert_alpha(),(self.blockWidth,
			self.blockHeight+10))
		screen.blit(waves,(x,y),area = None)
	elif self.waves[0][1] == 2:
		waves = pygame.transform.scale(pygame.image.load
			("images/wave2.png").convert_alpha(),(self.blockWidth,
			self.blockHeight+10))
		screen.blit(waves,(x,y),area = None)

def drawNumEnemies(self,screen):
	distance = 100
	x = (self.width-self.blockHeight)/2
	y = (self.height-self.blockHeight)/2-50
	myfont = pygame.font.SysFont("arial", self.blockHeight)
	enemies = "x "+ str(self.waves[0][0])
	numEnemies = myfont.render(enemies, 1, WHITE)
	screen.blit(numEnemies, (x,y+distance))

def drawCastle(self,screen):
	offset = self.width-self.cols*self.blockWidth
	castle = pygame.transform.scale(pygame.image.load
		("images/basement.png").convert_alpha(),(self.blockWidth+offset,
			self.blockHeight*3))
	(x, y) = (self.castle[1]*self.blockWidth,self.castle[0]*self.blockHeight)
	screen.blit(castle,(x,y), area=None)

def drawSoul(self,screen):
	if self.justDied != []:
		soul = pygame.transform.scale(pygame.image.load
			("images/soul.png").convert_alpha(),
			(self.blockWidth-10,self.blockHeight-5))
		screen.blit(soul, (self.justDied[0][0],self.justDied[0][1]), area=None)

def drawRange(self,screen):
	if self.displayRange == True:
		x = int(self.soldierDisplay[1]*self.blockHeight+0.5*self.blockHeight)
		y = int(self.soldierDisplay[0]*self.blockWidth+0.5*self.blockWidth)
		index = self.allSoldiers.index(self.soldierDisplay)
		if self.level[index] == 0:
			pygame.draw.circle(screen,BLUE2,(x,y),
				self.attackRange[self.soldierTypes[index]],2)
		elif self.level[index] == 1:
			boostedRange = self.boostedRange[self.soldierTypes[index]] 
			pygame.draw.circle(screen,BLUE2,(x,y),boostedRange,2)
		sellX = self.soldierDisplay[1]*self.blockHeight-self.sellSpace
		sellY = self.soldierDisplay[0]*self.blockWidth
		sell = pygame.transform.scale(pygame.image.load
			("images/sell.png").convert_alpha(),(self.blockWidth+10,
			self.blockHeight+10))
		screen.blit(sell,(sellX,sellY),area=None)
		# draw the upgrade arrow
		upgrade = pygame.transform.scale(pygame.image.load
			("images/upgrade.png").convert_alpha(),(self.blockWidth+10,self.blockHeight+10))
		upgradeX = self.soldierDisplay[1]*self.blockHeight+self.sellSpace
		upgradeY = self.soldierDisplay[0]*self.blockWidth
		screen.blit(upgrade,(upgradeX,upgradeY),area=None)
		# draw the number under the coin, so the user knows how much
		# he/she can sell the unit for
		myfont = pygame.font.SysFont("arial", self.blockHeight-10)
		# the price according to the type and level
		if self.level[index] == 0:
			price = int(0.8*self.price[self.soldierTypes[index]])
		elif self.level[index] == 1:
			price = int(0.8*(2*self.price[self.soldierTypes[index]]-20))
		sellPrice = myfont.render(str(price), 1, WHITE)
		screen.blit(sellPrice, (sellX+self.blockWidth-10,sellY+self.blockHeight-10))
		# get the price for upgrade
		if self.level[index] == 0:
			upgradePrice = myfont.render(str(int(self.price[self.soldierTypes[index]]-20)), 
				1, WHITE)
		elif self.level[index] == 1:
			upgradePrice = myfont.render(str("X"), 1, WHITE)
		screen.blit(upgradePrice, (upgradeX+self.blockWidth-10,sellY+self.blockHeight-10))

# images from my iphone game screenshots
def drawSoldiers(self, screen):
	swordsman1 = pygame.transform.scale(pygame.image.load
		("images/swordsman.png").convert_alpha(),(self.blockWidth-10,
		self.blockHeight-5))
	swordsman2 = pygame.transform.scale(pygame.image.load
		("images/swordsman2.png").convert_alpha(),(self.blockWidth-10,
		self.blockHeight-5))
	swordsman3 = pygame.transform.scale(pygame.image.load
		("images/swordsman3.png").convert_alpha(),(self.blockWidth-10,
		self.blockHeight-5))
	swordsman4 = pygame.transform.scale(pygame.image.load
		("images/swordsman4.png").convert_alpha(),(self.blockWidth-10,
		self.blockHeight-5))
	swordsmanLeft1 = pygame.transform.scale(pygame.image.load
		("images/swordsmanLeft1.png").convert_alpha(),(self.blockWidth-15,
			self.blockHeight-15))
	swordsmanLeft2 = pygame.transform.scale(pygame.image.load
		("images/swordsmanLeft2.png").convert_alpha(),(self.blockWidth-15,
			self.blockHeight-10))
	swordsmanLeft3 = pygame.transform.scale(pygame.image.load
		("images/swordsmanLeft3.png").convert_alpha(),(self.blockWidth-6,
			self.blockHeight-1))
	swordsmanLeft4 = pygame.transform.scale(pygame.image.load
		("images/swordsmanLeft4.png").convert_alpha(),(self.blockWidth-5,
			self.blockHeight))
	archer1 = pygame.transform.scale(pygame.image.load
		("images/archers.png").convert_alpha(),(self.blockWidth-10,
		self.blockHeight-5))
	archer2 = pygame.transform.scale(pygame.image.load
		("images/archers2.png").convert_alpha(),(self.blockWidth-10,
		self.blockHeight-5))
	archer3 = pygame.transform.scale(pygame.image.load
		("images/archers3.png").convert_alpha(),(self.blockWidth-10,
		self.blockHeight-5))
	archer4 = pygame.transform.scale(pygame.image.load
		("images/archers4.png").convert_alpha(),(self.blockWidth,
		self.blockHeight))
	archerLeft1 = pygame.transform.scale(pygame.image.load
		("images/archersLeft1.png").convert_alpha(),(self.blockWidth-13,
		self.blockHeight-9))
	archerLeft2 = pygame.transform.scale(pygame.image.load
		("images/archersLeft2.png").convert_alpha(),(self.blockWidth-8,
		self.blockHeight-3))
	archerLeft3 = pygame.transform.scale(pygame.image.load
		("images/archersLeft3.png").convert_alpha(),(self.blockWidth-13,
		self.blockHeight-8))
	archerLeft4 = pygame.transform.scale(pygame.image.load
		("images/archersLeft4.png").convert_alpha(),(self.blockWidth-6,
		self.blockHeight-4))
	wizard1 = pygame.transform.scale(pygame.image.load
		("images/wizards.png").convert_alpha(),(self.blockWidth-10,
		self.blockHeight-5))
	wizardLeft1 = pygame.transform.scale(pygame.image.load
		("images/wizardsLeft1.png").convert_alpha(),(self.blockWidth-10,
		self.blockHeight-5))
	wizard2 = pygame.transform.scale(pygame.image.load
		("images/wizards2.png").convert_alpha(),(self.blockWidth-10,
		self.blockHeight-5))
	wizardLeft2 = pygame.transform.scale(pygame.image.load
		("images/wizardsLeft2.png").convert_alpha(),(self.blockWidth-10,
		self.blockHeight-5))
	wizard3 = pygame.transform.scale(pygame.image.load
		("images/wizards3.png").convert_alpha(),(self.blockWidth-5,
		self.blockHeight))
	wizardLeft3 = pygame.transform.scale(pygame.image.load
		("images/wizardsLeft3.png").convert_alpha(),(self.blockWidth-3,
		self.blockHeight))
	wizard4 = pygame.transform.scale(pygame.image.load
		("images/wizards4.png").convert_alpha(),(self.blockWidth,
		self.blockHeight))
	wizardLeft4 = pygame.transform.scale(pygame.image.load
		("images/wizardsLeft4.png").convert_alpha(),(self.blockWidth,
		self.blockHeight))
	for pos in self.allSoldiers:
		index = self.allSoldiers.index(pos)
		if self.soldierTypes[index] == 0:
			# when the soldier is just standing there
			if pos not in self.attacking:
				if self.level[index] == 0:
					if self.soldierDir[index] == 1:
						swordsman = swordsman1
					else:
						swordsman = swordsmanLeft1
				elif self.level[index] == 1:
					if self.soldierDir[index] == 1:
						swordsman = swordsman2
					else:
						swordsman = swordsmanLeft2
				screen.blit(swordsman, (pos[1]*self.blockHeight+0.15*self.blockHeight,
					pos[0]*self.blockWidth+0.15*self.blockWidth), area=None)
			# while attacking
			else:
				if self.level[index] == 0:
					if self.soldierDir[index] == 1:
						attacking = swordsman3
					else:
						attacking = swordsmanLeft3
				elif self.level[index] == 1:
					if self.soldierDir[index] == 1:
						attacking = swordsman4
					else:
						attacking = swordsmanLeft4
				screen.blit(attacking, (pos[1]*self.blockHeight+0.15*self.blockHeight,
					pos[0]*self.blockWidth+0.15*self.blockWidth), area=None)
		elif self.soldierTypes[index] == 1:
			# while the archer is not attacking
			if pos not in self.attacking:
				if self.level[index] == 0:
					if self.soldierDir[index] == 1:
						archer = archer1
					else:
						archer = archerLeft1
				elif self.level[index] == 1:
					if self.soldierDir[index] == 1:
						archer = archer2
					else:
						archer = archerLeft2
				screen.blit(archer, (pos[1]*self.blockHeight+0.15*self.blockHeight,
					pos[0]*self.blockWidth+0.15*self.blockWidth), area=None)
			# while attacking
			else:
				if self.level[index] == 0:
					if self.soldierDir[index] == 1:
						attacking = archer3
					else:
						attacking = archerLeft3
				elif self.level[index] == 1:
					if self.soldierDir[index] == 1:
						attacking = archer4
					else:
						attacking = archerLeft4
				screen.blit(attacking, (pos[1]*self.blockHeight+0.15*self.blockHeight,
					pos[0]*self.blockWidth+0.15*self.blockWidth), area=None)
		elif self.soldierTypes[index] == 2:
			# not attacking
			if pos not in self.attacking:
				if self.level[index] == 0:
					if self.soldierDir[index] == 1:
						wizard = wizard1
					else:
						wizard = wizardLeft1
				elif self.level[index] == 1:
					if self.soldierDir[index] == 1:
						wizard = wizard2
					else:
						wizard = wizardLeft2
				screen.blit(wizard, (pos[1]*self.blockHeight+0.15*self.blockHeight,
					pos[0]*self.blockWidth+0.15*self.blockWidth), area=None)
			# attacking
			else:
				if self.level[index] == 0:
					if self.soldierDir[index] == 1:
						attacking = wizard3
					else:
						attacking = wizardLeft3
				elif self.level[index] == 1:
					if self.soldierDir[index] == 1:
						attacking = wizard4
					else:
						attacking = wizardLeft4
				screen.blit(attacking, (pos[1]*self.blockHeight
					+0.15*self.blockHeight-3,pos[0]*self.blockWidth+
					0.15*self.blockWidth-3), area=None)

# images from my iphone game screenshots
def drawEnemies(self, screen):
	enemy1 = pygame.transform.scale(pygame.image.load
		("images/enemy1.png").convert_alpha(),
		(self.blockWidth-10,self.blockHeight-5))
	enemy2 = pygame.transform.scale(pygame.image.load
		("images/enemy2.png").convert_alpha(),
		(self.blockWidth-10,self.blockHeight-5))
	enemy3 = pygame.transform.scale(pygame.image.load
		("images/enemy3.png").convert_alpha(),
		(self.blockWidth-10,self.blockHeight))
	for enemies in self.allEnemies:
		if self.waves[0][1] == 0:
			screen.blit(enemy1, (enemies[0],enemies[1]), area=None)
			index = self.allEnemies.index(enemies)
			fraction = self.enemyHealth[index]/self.health[0]
			# assign the health bar
			if fraction > 1/2:
				pygame.draw.rect(screen,GREEN2,(enemies[0],enemies[1]-5,
					(self.blockWidth-10)*fraction,5))
			elif 1/4 <= fraction <= 1/2:
				pygame.draw.rect(screen,YELLOW,(enemies[0],enemies[1]-5,
					(self.blockWidth-10)*fraction,5))
			else:
				pygame.draw.rect(screen,RED,(enemies[0],enemies[1]-5,
					(self.blockWidth-10)*fraction,5))
		elif self.waves[0][1] == 1:
			screen.blit(enemy2, (enemies[0],enemies[1]), area=None)
			index = self.allEnemies.index(enemies)
			fraction = self.enemyHealth[index]/self.health[1]
			# assign the health bar
			if fraction > 1/2:
				pygame.draw.rect(screen,GREEN2,(enemies[0],enemies[1]-5,
					(self.blockWidth-10)*fraction,5))
			elif 1/4 <= fraction <= 1/2:
				pygame.draw.rect(screen,YELLOW,(enemies[0],enemies[1]-5,
					(self.blockWidth-10)*fraction,5))
			else:
				pygame.draw.rect(screen,RED,(enemies[0],enemies[1]-5,
					(self.blockWidth-10)*fraction,5))
		elif self.waves[0][1] == 2:
			screen.blit(enemy3, (enemies[0],enemies[1]-5), area=None)
			index = self.allEnemies.index(enemies)
			fraction = self.enemyHealth[index]/self.health[2]
			# assign the health bar
			if fraction > 1/2:
				pygame.draw.rect(screen,GREEN2,(enemies[0],enemies[1]-5,
					(self.blockWidth-10)*fraction,5))
			elif 1/4 <= fraction <= 1/2:
				pygame.draw.rect(screen,YELLOW,(enemies[0],enemies[1]-5,
					(self.blockWidth-10)*fraction,5))
			else:
				pygame.draw.rect(screen,RED,(enemies[0],enemies[1]-5,
					(self.blockWidth-10)*fraction,5))

# imgaes from google search
def drawMap(self, screen):
	dimension = (self.blockWidth, self.blockHeight)
	ratioFactor = (dimension[0]*0.15,dimension[1]*0.15)
	grass = pygame.transform.scale(pygame.image.load
		("images/grass.jpeg").convert_alpha(),(self.width,self.height))
	screen.blit(grass, (0,0), area=None)
	stoneTiles = pygame.transform.scale(pygame.image.load
		("images/stoneTile.jpeg").convert_alpha(),(dimension[0],dimension[1]))
	for row in range(self.rows):
		for col in range(self.cols):
			location = (col*self.blockWidth, row*self.blockHeight)
			if self.map[row][col] == 1:
				screen.blit(stoneTiles,(location[0],location[1]))
			if self.map[row][col] == 2:
				location2 = (col*self.blockWidth+ratioFactor[0],
					row*self.blockHeight+ratioFactor[1])
				dimension2 = (self.blockWidth*0.85, self.blockHeight*0.85)
				pygame.draw.rect(screen, BLUE, (location2, dimension2), 1)

def drawSelected(self, screen):
	if self.lastClick != []:
		location = (self.lastClick[0][1]*self.blockWidth+0.15*self.blockWidth,
			self.lastClick[0][0]*self.blockHeight+0.15*self.blockHeight)
		pygame.draw.rect(screen, BLUE2, (location, (self.blockWidth*0.85,
			self.blockHeight*0.85)))
		# location of the swordmen picture
		locSword = (self.soldierX,self.soldierY)
		sword = pygame.transform.scale(pygame.image.load
			("images/sword.png").convert_alpha(),(self.soldierSizeX,
			self.soldierSizeY))
		screen.blit(sword, locSword, area=None)
		# location of the archers picture
		locArcher = (self.soldierX+self.soldierSizeX+self.soldierSpace,self.soldierY)
		archer = pygame.transform.scale(pygame.image.load
			("images/archer.png").convert_alpha(),(self.soldierSizeX,
			self.soldierSizeY))
		screen.blit(archer, locArcher, area=None)
		# location of the wizards picture
		locWizard = (self.soldierX+self.soldierSizeX*2+2*self.soldierSpace,
			self.soldierY)
		wizard = pygame.transform.scale(pygame.image.load
			("images/wizard.png").convert_alpha(),(self.soldierSizeX,self.soldierSizeY))
		screen.blit(wizard, locWizard, area=None)

# images are all screenshots from my iphone game
def drawIcons(self, screen):
	iconSize = 50
	topIconSize = 40
	dRatio = 1.8
	leftSpace = 150
	if self.gameStopped:
		startArrow = pygame.transform.scale(pygame.image.load
			("images/startArrow.png").convert_alpha(),(iconSize,iconSize))
		screen.blit(startArrow, (self.keySpace,self.keyY), area=None)
	else:
		pause = pygame.transform.scale(pygame.image.load
			("images/pause.png").convert_alpha(),(iconSize,iconSize))
		screen.blit(pause, (self.keySpace,self.keyY) ,area=None)
	if self.fastForward == False:
		forward = pygame.transform.scale(pygame.image.load
			("images/forward.png").convert_alpha(),(iconSize+30,iconSize))
		screen.blit(forward, (self.keySpace+dRatio*iconSize-10,self.keyY),area=None)
	else:
		forward2 = pygame.transform.scale(pygame.image.load
			("images/forward2.png").convert_alpha(),(iconSize+45,iconSize+7))
		screen.blit(forward2, (self.keySpace+dRatio*iconSize-20,self.keyY-5),
			area=None)
	menu = pygame.transform.scale(pygame.image.load
		("images/taiji.png").convert_alpha(),(iconSize,iconSize))
	screen.blit(menu, (self.keySpace+2*dRatio*iconSize,self.keyY) ,area=None)
	coin = pygame.transform.scale(pygame.image.load
		("images/coin2.png").convert_alpha(),(topIconSize, topIconSize))
	screen.blit(coin, (self.keySpace,self.keyY2), area=None)
	heart = pygame.transform.scale(pygame.image.load
		("images/heart.png").convert_alpha(),(topIconSize, topIconSize))
	screen.blit(heart, (self.width-leftSpace,self.keyY2), area=None)
	# display the number of lives left next to the heart
	myfont = pygame.font.SysFont("arial", self.blockHeight)
	lives = myfont.render(str(self.lives), 1, WHITE)
	screen.blit(lives, (self.width-leftSpace+2*self.keySpace,self.keyY2))
	gold = myfont.render(str(self.money), 1, WHITE)
	screen.blit(gold, (2*self.keySpace+topIconSize,self.keyY2))
	# waves
	waves = pygame.transform.scale(pygame.image.load
		("images/waveCount.png").convert_alpha(),(topIconSize, topIconSize))
	screen.blit(waves, (self.width-leftSpace-self.keySpace-4*topIconSize,
		self.keyY2), area=None)
	wave = myfont.render(str(self.totalWaves-len(self.waves))+
		" / "+str(self.totalWaves), 1, WHITE)
	screen.blit(wave, (self.width-leftSpace-3*topIconSize,
		self.keyY2))
	# draw clickHere
	if self.hint == True:
		clickHere = pygame.transform.scale(pygame.image.load
			("images/clickHere.png").convert_alpha(),(self.clickSize,self.clickSize))
		screen.blit(clickHere, (self.keySpace+2*dRatio*iconSize+10,self.keyY+10),
			area=None)

Game(820 , 820).run()