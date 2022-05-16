import pygame, sys, random
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.display.set_caption("Save the World")
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
BACKGD_COLOUR = (230, 255, 250)
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

enemy_image = pygame.image.load("Assets/enemy.png").convert_alpha()
enemies_image_tr = pygame.transform.scale(enemy_image, (50,25))

bullet_sound = pygame.mixer.Sound("Assets/shoot.wav")

pygame.mixer.music.load('Assets/shoot.wav')
pygame.mixer.music.play()


stars_image = pygame.image.load ("Assets/stars.jpg").convert()
stars_image_tr = pygame.transform.scale(stars_image, (SCREEN_WIDTH,SCREEN_HEIGHT))


player_image = pygame.image.load("Assets/avatar.png").convert()

space = pygame.image.load("Assets/meteormaker.png").convert()
sc_img = pygame.transform.scale(space, (960, 100))


# image should not have been converted with convert_alpha(0 but with convert()
player_image.set_colorkey((255,255,255))
clock = pygame.time.Clock()

Ui_font = pygame.font.SysFont("arial", 25)

# Ship 1

class AlienShipOne:
	def __init__(self, x, y, spd):
		self.x = x
		self.y = y
		self.movespeed = spd

	def move(self):

		self.x += self.movespeed

		if self.x >= SCREEN_WIDTH - 50 or self.x <= 50:

			self.movespeed *= -1
			self.y = self.y + 130

	def draw(self):
		screen.blit(enemies_image_tr, (self.x, self.y))

	def createSpaceship(self):
		alienship.append(Laser(random.randint(self.x, self.x+50), self.y+50))

	def collide(self, bullet):
		return pygame.Rect(self.x, self.y, 50, 50).collidepoint((bullet.x, bullet.y))

	def collides(self, ship):
		return pygame.Rect(self.x, self.y, 50, 50).collidepoint((ship.x, ship.y))


# Player
class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = player_image
		self.rect = self.image.get_rect()
		self.rect.center = (480, 490)
		self.health = 3

	def update(self):

		if pressed_keys[K_RIGHT] and self.rect.x <SCREEN_WIDTH - 60:
			self.rect.x += 5

		if pressed_keys[K_LEFT] and self.rect.x > 0:
			self.rect.x -= 5

	def meteor_hit(self):
		return pygame.Rect(self.rect.x, self.rect.y).collidepoint((rock))

	def createbullet(self):
		bullets.append(Bullet(self.rect.x + 10, self.rect.y))

# Projectile
class Laser:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.velo = random.randint(1, 10)
		self.accel = random.randint(1, 10)

	def move(self):
		self.y += self.accel

	def draw(self):
		pygame.draw.circle(screen, (150, 150, 150), (self.x, self.y), 2)


class Bullet:

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def move(self):
		self.y -= 5

	def draw(self):
		pygame.draw.line(screen, (0, 255, 0), (self.x, self.y), (self.x, self.y - 10), 4)

	def collide(self, ship):
		return pygame.Rect(self.x, self.y, 50, 50).collidepoint((ship.x, ship.y))


	def collide(self, rok):
		return pygame.Rect(self.x, self.y, 50, 50).collidepoint((rok.x, rok.y))

	# def collides(self, player):
	# 	return pygame.Rect(self.x, self.y, 50, 50).collidepoint((player.x, player.y))


# Space Debris
class Meteor:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.speed = random.randint(1, 2)

	def move(self):
		self.y += self.speed

	def draw(self):
		pygame.draw.circle(screen, (150, 150, 150), (self.x, self.y), 33)

	def collide(self, rok):
		return pygame.Rect(self.x, self.y, 50, 50).collidepoint((rok.x, rok.y))

class Asteroid:

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def draw(self):
		screen.blit(sc_img, (self.x, self.y - 150))

	def create_meteor(self):
		meteors.append(Meteor(random.randint(self.x + 0, self.x + 30000), self.y + 10))


alienship = []

bullets = []

ships = []

meteors = []

rocks1 = Asteroid(1, 5)

for i in range(1, 10):
	# ships.append(AlienShipOne(10 + (i * 75), -130, 1.5))
	#
	# ships.append(AlienShipOne(10 + (i * 75), -65, 1.5))

	ships.append(AlienShipOne(10 + (i*75),0, 1.5))

	# ships.append(AlienShipOne(10 + (i*75),65, 1.5))


player = Player()

playerGroup = pygame.sprite.Group()

playerGroup.add(player)


while 1:
	#pygame registers all events from the users into an event queue
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			player.createbullet()
			bullet_sound.play()


	pressed_keys = pygame.key.get_pressed()

# Update
	playerGroup.update()

# Rendering
	screen.fill(BACKGD_COLOUR)

	screen.blit(stars_image_tr, (0, 0))

	rocks1.create_meteor()

	playerGroup.draw(screen)

	for bullet in bullets:
		bullet.move()
		bullet.draw()
		for ship in ships:
			if ship.collide(bullet):
				bullets.remove(bullet)
				ships.remove(ship)
		for rok in meteors:
			if rok.collide(bullet):
				bullets.remove(bullet)
				meteors.remove(rok)


	for ship in ships:
		ship.draw()
		ship.move()

	for rock in meteors:
		rock.draw()
		rock.move()
		if player.meteor_hit():
			print("HIT")

	rocks1.draw()



	pygame.display.flip()