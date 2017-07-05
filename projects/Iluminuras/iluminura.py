import cv2
import numpy as np
import random as r
from collections import deque
import math as m


r.seed()

height = 768
width = 1024
seed_count = 15

slate = np.zeros((height,width,3), np.uint8)


# lista de pontos, x, y, vetor direcao, count
point_list = deque()
auxcount = 0

for i in range(seed_count):
	point_list.append(( r.randint(0, width), r.randint(0, height), (float(r.random()), r.random()), 0))

while point_list:
	x, y, direction, count = point_list.popleft()
	points = np.array([[x, y], [x+ 5*direction[0], y+ 5*direction[1]]], dtype=np.int32)
	
	if r.randint(0,1) == 0:
		dirx = -m.sin(count)
		diry = m.cos(count)
		direction = (dirx, diry)
	else:
		count += r.random();
	
	if (0<= points[0][0] <= width) and (0<= points[0][1] <= height):
		point_list.append((  points[1][0], points[1][1], direction, count+1 ))
	else:
		continue
		
	cv2.polylines(slate, np.int32([points]) , 1, (255,255,255), 1)
	
	
	if auxcount %50 ==0:
		cv2.imshow("window", slate)
		cv2.waitKey(5)
	auxcount+=1

cv2.imshow("window", slate)
cv2.waitKey(0)