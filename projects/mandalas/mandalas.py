import cv2
import numpy as np
import random as r
from collections import deque
import math as m

r.seed()

height = 600
width = 1200

vertix_mode = False

angle = 2
step_angle = 360//angle

slate = np.zeros((height,width,3), np.uint8)

replicate = 5

max_depth = 2

scaledown_rate = .5

def midpoint(pointa, pointb):
	xa, ya = pointa
	xb, yb = pointb
	return (xa+xb)//2, (ya+yb)//2
	
def draw_rec_circle(center, radius, depth, color):
	
	if depth >= max_depth:
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
	
	for i in range(replicate):
		if vertix_mode:
			draw_rec_circle(points[i*step], int(radius * scaledown_rate), depth+1, color)
		else:
			draw_rec_circle(midpoint(points[i*step], points[(i+1)*step]), int(radius * scaledown_rate), depth+1, color)


draw_rec_circle((width//2, height//2), 150, 0, (120,200,200))

hsv = cv2.cvtColor(slate, cv2.COLOR_HSV2BGR)
cv2.imshow("window", hsv)
cv2.waitKey(0)