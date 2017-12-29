import pygame
import math

class Soldier(pygame.sprite.Sprite):
	def __init__(self,row,col,blockWidth,blockHeight,attackRange,damage,gold):
		super(Soldier, self).__init__()
		self.attackRange = attackRange
		self.damage = damage
		self.blockWidth = blockWidth
		self.blockHeight = blockHeight
		self.row = row
		self.col = col
		self.gold = gold

	def getPos(self):
		return (self.row,self.col)

	def getXY(self):
		x = self.col*self.blockWidth+0.5*self.blockWidth
		y = self.row*self.blockHeight+0.5*self.blockHeight
		return (x,y)

	# the soldiers able to cause damage
	def attack(self,allEnemies,justDied,enemyHealth,deadEnemies,level,
		soldierTypes,allSoldiers,attacking,direction,wizardBall,archerArrow):
		attackBoost = [45,29,24]
		rangeBoost= [100,140,160]
		# for all the enemies
		for enemy in allEnemies:
			soldierX = self.getXY()[0]
			soldierY = self.getXY()[1]
			distance1 = ((soldierX-enemy[0])**2+(soldierY-enemy[1])**2)**0.5
			distance2 = ((soldierX-(enemy[0]+self.blockWidth-10))**2+(soldierY-
				enemy[1])**2)**0.5
			distance3 = ((soldierX-enemy[0])**2+(soldierY-(enemy[1]+
				self.blockHeight-5))**2)**0.5
			distance4 = ((soldierX-(enemy[0]+self.blockWidth-10))**2+(soldierY-
				(enemy[1]+self.blockHeight-5))**2)**0.5
			# any of the four corners in range
			distance = min(distance1,distance2,distance3,distance4)
			

			if level != []:
				index = allSoldiers.index((self.row,self.col))
				if level[index] == 1 or level[index] == 3:
					# cause attack for different level
					if soldierTypes[index] == 0:
						self.damage = attackBoost[0]
						self.attackRange = rangeBoost[0]
						
					elif soldierTypes[index] == 1:
						self.damage = attackBoost[1]
						self.attackRange = rangeBoost[1]
					elif soldierTypes[index] == 2:
						self.damage = attackBoost[2]
						self.attackRange = rangeBoost[2]
			# cause damage
			if distance <= self.attackRange:
				# find which way the soldier suppose to face
				if level != []:
					if soldierX-enemy[0] >= 0:
						direction.pop(index)
						direction.insert(index,-1)
					else:
						direction.pop(index)
						direction.insert(index,1)
				# find the angle between the arrow and the soldier
				a1 = enemy[0]-soldierX
				a2 = -(enemy[1]-soldierY)
				# a is the vector with the tail at the soldier and the head
				# at the enemy
				a = [a1, a2]
				# b is the vector pointing in theArrow's direction
				b = [1, 0]
				cosTheta = ((a[0]*b[0]+a[1]*b[1])/
					((a[0]**2+a[1]**2)**0.5*(b[0]**2+b[1]**2)**0.5))
				# the angle theArrow should rotate
				theta = math.acos(cosTheta)*180/math.pi
				if soldierY - enemy[1] < 0:
					theta = 360-theta

				x, y = enemy[0], enemy[1]
				index = allEnemies.index(enemy)
				health = enemyHealth[index]
				newHealth = health - self.damage
				x = self.getPos()[1]*self.blockWidth+0.5*self.blockWidth
				y = self.getPos()[0]*self.blockHeight+0.5*self.blockHeight
				# sound effect
				count = allSoldiers.index((self.row,self.col))
				if soldierTypes[count] == 0:
					effect = pygame.mixer.Sound('images/cut.wav')
					effect.play()
				elif soldierTypes[count] == 1:
					effect = pygame.mixer.Sound('images/archerShoot.wav')
					effect.play()
					# get the archers to have arrows
					archerArrow.append([x,y,enemy[0],enemy[1],count,theta])
				elif soldierTypes[count] == 2:
					effect = pygame.mixer.Sound('images/wizardShoot.wav')
					effect.play()
					wizardBall.append([x,y,enemy[0],enemy[1],count])
				attacking.append(self.getPos())
				enemyHealth[index] = newHealth

				# if killed, pop the unit
				if newHealth <= 0:
					justDied.append(allEnemies.pop(index))
					deadEnemies.append(justDied[0])
					enemyHealth.pop(index)
					self.gold.append(10)
				break

# different types of soldiers
class Swordsman(Soldier):
	def __init__(self,row,col,blockWidth,blockHeight,attackRange,damage,gold):
		super(Swordsman, self).__init__(row,col,blockWidth,blockHeight,
			attackRange,damage,gold)

class Archer(Soldier):
	def __init__(self,row,col,blockWidth,blockHeight,attackRange,damage,gold):
		super(Archer, self).__init__(row,col,blockWidth,blockHeight,
			attackRange,damage,gold)

class Wizard(Soldier):
	def __init__(self,row,col,blockWidth,blockHeight,attackRange,damage,gold):
		super(Wizard, self).__init__(row,col,blockWidth,blockHeight,
			attackRange,damage,gold)
			