import pygame
import utils

from classes import *
from pygame.locals import *


fps = 30

player = True
training = False
leveleditor = False
neural = True
DEBUG = True

if(neural):
	import neuralnet

print ( "start")

move = 0
map = "map1"

inputs = []
outputs = []


true_stopped = False
while not true_stopped:
	stopped = False
	up = down = left = right = False
	collision = False

	pygame.init()
	screen = pygame.display.set_mode((1024,720))
	pygame.display.set_caption('nn-car')
	clock = pygame.time.Clock()




	drawables = []
	car = Car(Pos((100,100)),0)
	for pos,rot,type in utils.load(map):
		if type == "blockade":
			#drawables.append(Blockade(pos,rot))
			pass
		elif type == "car":
			car = Car(pos,rot)
		elif type[:3] == "map": #so map_1.png refers to the image 1.png
			backgroundmap = Map(type)

	while not stopped:
		dt = clock.get_time()/30
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
				stopped = True
				true_stopped = True
			if DEBUG:
				if event.type != pygame.MOUSEMOTION:
					if event.type == pygame.MOUSEBUTTONDOWN:
						bcol.red(event.pos)
			if player:
				if event.type == pygame.KEYDOWN:
					if   event.key == K_UP:    up    = True
					elif event.key == K_DOWN:  down  = True
					elif event.key == K_LEFT:  left  = True
					elif event.key == K_RIGHT: right = True
				if event.type == pygame.KEYUP:
					if   event.key == K_UP:    up    = False
					elif event.key == K_DOWN:  down  = False
					elif event.key == K_LEFT:  left  = False
					elif event.key == K_RIGHT: right = False
			if leveleditor:
				if event.type == pygame.MOUSEBUTTONDOWN:
					elem = utils.get_closest(drawables,Pos(event.pos))
					if event.button == 1:
						move = elem
					if event.button == 2:
						bpos = Pos(event.pos)
						drawables.append(Blockade(bpos,0))
					elif event.button == 3:
						drawables.remove(elem)
					elif event.button == 4:
						elem.rot += utils.rad(15)
					elif event.button == 5:
						elem.rot -= utils.rad(15)
				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						move = 0
				if move != 0:
					move.pos = Pos(event.pos)

		r = [car.rays[0].range, car.rays[1].range, car.rays[2].range, car.rays[3].range, car.rays[4].range]
		if neural:
			power,turn = neuralnet.predict(r)
			up    = (power == 1)
			down  = (power == 2)
			left  = (turn  == 1)
			right = (turn  == 2)
			if collision:
				stopped = True
		if training:
			inputs.append(r)
			if up-down == 1:
				nnpower = 1 #forward
			if up-down == 0:
				nnpower = 0 #no power
			if up-down == -1:
				nnpower = 2 #back
			if left-right == 1:
				nnsteer = 1 #left
			if left-right == 0:
				nnsteer = 0 #no steer
			if left-right == -1:
				nnsteer = 2 #right
			outputs.append([nnpower,nnsteer])

		screen.fill((200,200,200))
		collision = bool(car.check_collision(drawables))
		if not collision:
			if up    : car.accelerate(1,dt)
			if down  : car.accelerate(-3,dt)
			if left  : car.turn(1,dt)
			if right : car.turn(-1,dt)

		car.step(collision,dt)
		backgroundmap.draw(screen)
		for elem in drawables:
			elem.draw(screen)
		car.raycast(screen)
		car.draw(screen)

		pygame.display.flip()
		pygame.display.update()
		clock.tick(fps)
		pygame.display.set_caption('nn-car ' + utils.format(clock.get_fps()))
		#print("frame")
	pygame.quit()

	if neural and not true_stopped:
		fitness = car.pos.x
		print(fitness)



if training:
	utils.save_training("tdata",inputs,outputs)
if leveleditor:
	drawables.append(car) #also save the car
	drawables.append(backgroundmap)
	utils.save(map,drawables)
quit()
