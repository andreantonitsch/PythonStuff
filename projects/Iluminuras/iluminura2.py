import cv2
import numpy as np
import random as r
from collections import deque
import math as m


r.seed()

height = 668
width = 1024
seed_count = 3

ellipse_axes_long = [20,45]
ellipse_axes_short = [14,30]
min_angle = 0
max_angle = 360

slate = np.zeros((height,width,3), np.uint8)

color = (255,255,255)

# lista de pontos, x, y, vetor direcao, count
point_list = deque()
auxcount = 0



for i in range(seed_count):
	point_list.append(( r.randint(0, width), r.randint(0, height), 0))

while point_list:
	x, y, count = point_list.popleft()
	
	if count % 7 == 0:
		point_list.append((x, y, count+r.randint(1, 3) ))
	if count % 37 == 0:
		continue
		
	points = cv2.ellipse2Poly((x,y),
                              (r.randint(ellipse_axes_long[0],ellipse_axes_long[1]), r.randint(ellipse_axes_short[0],ellipse_axes_short[1])),
                               r.randint(min_angle, max_angle),
							   r.randint(0,360),
							   r.randint(0,360), 15) #angle between points
	
	point_delta_x = x - points[0][0]
	point_delta_y = y - points[0][1]
	
	for i in points:
		i[0] += point_delta_x
		i[1] += point_delta_y
		
	
	
	if (0<= points[0][0] <= width) and (0<= points[0][1] <= height):
		point_list.append((points[-1][0], points[-1][1], count+r.randint(1, 3) ))
	else:
		continue
		
	cv2.polylines(slate, np.int32([points]) , 0, color, 1)
	
	color = ((color[0] + r.randint(0, 20)) % 256, (color[1] + r.randint(0, 20)) % 256, (color[2] + r.randint(0, 20)) % 256)
	
	#if auxcount %50 ==0:
	cv2.imshow("window", slate)
	cv2.waitKey(1)
	auxcount+=1

cv2.imshow("window", slate)
cv2.waitKey(0)