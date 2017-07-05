import cv2
import numpy as np
import random as r
from collections import deque
import math as m

while True:
	r.seed()

	height = 600
	width = 1200
	seed_count = 3

	stack_mode = False
	
	square_mode = False
	with_straights = False
	
	slate = np.zeros((height,width,3), np.uint8)

	# lista de pontos, x, y, color, x0, y0
	point_list = deque()
	auxcount = 0

	radius = 8
	angpoints = 1
	step_angle = 120 #Algum divisor de 360 >= 45 e <180
	arc_divisor = int(360/step_angle)
	
	
	length_path = 10
	path_angle = 90
	directions = {0:(length_path,0), 1:(0,length_path), 2:(-length_path,0), 3:(0,-length_path)}
	
	
	# cada ponto é uma tupla: x, y, colorHSV
	for i in range(seed_count):
		point_list.append(( r.randint(0, width), r.randint(0, height), (0, 200, 200)))

	while point_list:
		if stack_mode:
			x, y, color= point_list.pop()
		else:
			x, y, color = point_list.popleft()
		h, s, v = color
		h = (h+1) % 180
		color = h,s,v
		
		if r.randint(0,2) == 0:
			point_list.append((x, y, color))
	#	if r.randint(0,47) == 0:
		#	continue
		
		direction  = r.randint(0,3)	
		
		drawn = False
		attempts = 0

		while not drawn:
			
			points = [[x,y], [x + directions[direction][0], y+directions[direction][1]]]

			if 0 <= points[-1][0] < width and 0 <= points[-1][1] < height: 
				if slate[points[-1][1]][points[-1][0]][2] == 0:

					cv2.polylines(slate, np.int32([points]) , 0, color, 1)
					
					drawn = True
			if attempts > 3:
				break
			attempts  += 1
			direction += 1
			direction %= 4
			
		if not drawn:
			continue
					
		if (0<= points[-1][0] <= width) and (0<= points[-1][1] <= height):
		#	if h == 0 or h == 179:
		#		color = (h, s+1, v)
		#		
		#	if s %2 ==1:
		#		color = (h-2, s, v)
		#	else:
		#		color = (h+2, s, v)
			point_list.append((points[-1][0], points[-1][1], color))
			
		else:
			continue
		
		if auxcount % 200 == 0:
			hsv = cv2.cvtColor(slate, cv2.COLOR_HSV2BGR)
			cv2.imshow("window", hsv)
			cv2.waitKey(1)
		auxcount+=1

hsv = cv2.cvtColor(slate, cv2.COLOR_HSV2BGR)
cv2.imshow("window", hsv)
cv2.waitKey(0)