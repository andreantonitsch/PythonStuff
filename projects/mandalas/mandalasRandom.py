import cv2
import numpy as np
import random as r
from collections import deque
import math as m

r.seed()

vertix_mode = True

height = 600
width = 1200

sides = 1
step_angle = 360//sides

slate = np.zeros((height,width,3), np.uint8)

replicate = 4

max_depth = 6

scaledown_rate = .2

def midpoint(pointa, pointb):
	xa, ya = pointa
	xb, yb = pointb
	return (xa+xb)//2, (ya+yb)//2

def draw_rec_circle(center, radius, depth, color):
	
	if depth > max_depth:
		return
	
	h, s, v = color
	h = (h+20) % 180
	color = h,s,v
	
	x , y = center

	points = cv2.ellipse2Poly((x,y),
							  (radius, radius),
							   0,
							   0 ,
							   360,
							   step_angle) #angle between points

	cv2.polylines(slate, np.int32([points]) , 0, color, 1)
	
	step = len(points) // replicate
	#step = replicate
	
	for i in range(replicate):
		if vertix_mode:
			draw_rec_circle(points[i*step], int(radius * scaledown_rate), depth+1, color)
		else:
			draw_rec_circle(midpoint(points[i*step], points[((i+1)*step) % len(points)]) , int(radius * scaledown_rate), depth+1, color)
count = 0
while True:

	sides = r.randint(3,10)
	step_angle = 360//sides
	
	vertix_mode = r.randint(0,1)
	
	slate = np.zeros((height,width,3), np.uint8)

	#replicate = r.randint(1,angle)
	replicate  = sides
	
	max_depth = r.randint(1,4)

	scaledown_rate = r.random()

	draw_rec_circle((width//2, height//2), 150, 0, (120,200,200))

	hsv = cv2.cvtColor(slate, cv2.COLOR_HSV2BGR)

	cv2.imwrite("temp/"+str(count) + ".png", hsv)
	count += 1
	
	cv2.imshow("window", hsv)
	cv2.waitKey(1000)
	count+= 1