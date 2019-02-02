import pygame
import math
import utils

DEBUG = False

class Drawable(pygame.sprite.Sprite):
	def __init__(self,img_path,pos,rot):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(img_path)
		self.rot = rot
		self.pos = pos
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()
		self.rect.center = self.pos.tuple()

	def draw(self,screen):
		rotated = pygame.transform.rotate(self.image,self.rot/(2*math.pi)*360)
		self.rect = rotated.get_rect()
		self.rect.center = self.pos.tuple()
		screen.blit(rotated,self.rect)
		self.mask = pygame.mask.from_surface(rotated)
		if DEBUG:

			pygame.draw.rect(screen,(200,0,0),self.rect,1)
			pygame.draw.lines(screen,(0,200,0),1,self.mask.outline())
	def toString(self):
		return "drawable"

class Car(Drawable):

	def __init__(self,pos,rot):
		Drawable.__init__(self,"car_small.png",pos,rot)
		self.steer_coef = 0.05
		self.steer_growth = 0.5
		
		self.acc_coef = 0.4
		self.dec_coef = -0.02
		
		self.vel_min = 0
		self.vel_max = 5
		
		self.vel = 0
		
		self.rays = [Ray(1,pos,pos),Ray(1,pos,pos),Ray(1,pos,pos),Ray(1,pos,pos),Ray(1,pos,pos)]

	def step(self,collision,dt):
		self.accelerate(self.dec_coef,dt)
		if collision:
			self.vel = -0.5
		self.pos.x += math.cos(self.rot)*self.vel*dt
		self.pos.y += math.sin(-self.rot)*self.vel*dt

	def check_collision(self,drawables):
		collisions = pygame.sprite.spritecollide(self,drawables,False)
		collidable = pygame.sprite.collide_mask
		return pygame.sprite.spritecollideany(self,collisions,collidable)

	def accelerate(self,p,dt):
		p = max(-3,min(1,p))

		self.vel += p*self.acc_coef*dt

		self.vel = max(self.vel_min,min(self.vel_max,self.vel))

	def turn(self,r,dt):
		r = max(-1,min(r,1))

		self.rot += r*self.steer_coef*(self.vel/(self.vel_max*self.steer_growth)+1-self.steer_growth)*dt

		if self.rot > math.pi:
			self.rot = -math.pi
		if self.rot < -math.pi:
			self.rot = math.pi
		self.accelerate(-0.1,dt)

	def toString(self):
		return "car"

	def raycast(self,screen,angle = 45):
		r1,c1 = utils.ray(screen, self.pos, self.rot+utils.rad(angle ))
		r2,c2 = utils.ray(screen, self.pos, self.rot+utils.rad(angle/2 ))
		r3,c3 = utils.ray(screen, self.pos, self.rot                  )
		r4,c4 = utils.ray(screen, self.pos, self.rot+utils.rad(-angle/2))
		r5,c5 = utils.ray(screen, self.pos, self.rot+utils.rad(-angle))

		ray1 = Ray(r1,c1,self.pos)
		ray2 = Ray(r2,c2,self.pos)
		ray3 = Ray(r3,c3,self.pos)
		ray4 = Ray(r4,c4,self.pos)
		ray5 = Ray(r5,c5,self.pos)

		self.rays = [ray1,ray2,ray3,ray4,ray5]

	def draw(self,screen):
		Drawable.draw(self,screen)
		for r in self.rays:
			r.draw(screen)

class Blockade(Drawable):
	def __init__(self,pos,rot):
		Drawable.__init__(self,'blockade.png',pos,rot)

	def toString(self):
		return "blockade"
		
class Map(Drawable):
	def __init__(self,filename):
		Drawable.__init__(self,filename[4:],Pos((1024/2,720/2)),0)
		self.filename = filename

	def toString(self):
		return self.filename;

class Ray:
	def __init__(self,range,point,origin):
		self.range = range
		self.point = point
		self.origin = origin
	def draw(self,screen):
		pygame.draw.lines(screen,((self.range)*255,(1-self.range)*255,0),5,[self.point.tuple(),self.origin.tuple()])
	def toString(self):
		return self.origin.toString() + " :  " + self.point.toString() + " : " + str(self.range)

class Pos:
	def __init__(self,p):
		self.x = float(p[0])
		self.y = float(p[1])
	def tuple(self):
		return (int(self.x),int(self.y))
	def toString(self):
		return utils.format(self.x,2)+":"+utils.format(self.y,2)
	def dist(self,pos):
		return math.sqrt((pos.x-self.x)**2+(pos.y-self.y)**2)
	def smaller_than(self,pos):
		return self.x <= pos.x or self.y <= pos.y
	def copy(self):
		return Pos((self.x,self.y))

class bcol:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

	@staticmethod
	def blue(txt):
		print(bcol.OKBLUE, end='')
		print(txt,end='')
		print(bcol.ENDC)
	@staticmethod
	def green(txt):
		print(bcol.OKGREEN, end='')
		print(txt,end='')
		print(bcol.ENDC)
	@staticmethod
	def yellow(txt):
		print(bcol.WARNING, end='')
		print(txt,end='')
		print(bcol.ENDC)
	@staticmethod
	def purple(txt):
		print(bcol.HEADER, end='')
		print(txt,end='')
		print(bcol.ENDC)
	@staticmethod
	def red(txt):
		print(bcol.FAIL, end='')
		print(txt,end='')
		print(bcol.ENDC)
