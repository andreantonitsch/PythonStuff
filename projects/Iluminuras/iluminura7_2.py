import cv2
import numpy as np
import random as r
from collections import deque
import math as m

while True:
	r.seed()

	height = 600
	width = 1200
	seed_count = 1

	stack_mode = False
	
	square_mode = True
	with_straights = False
	slate = np.zeros((height,width,3), np.uint8)

	# lista de pontos, x, y, color, x0, y0
	point_list = deque()
	auxcount = 0

	radius = 8
	angpoints = 1
	step_angle = 60 #Algum divisor de 360 >= 45 e <180
	arc_divisor = int(360/step_angle)
	
	# cada ponto é uma tupla: x, y, colorHSV, x0, y0
	for i in range(seed_count):
		point_list.append(( r.randint(0, width//radius)*radius, r.randint(0, height//radius)*radius, (0, 200, 200), 0 , 0))
		# point_list.append(( r.randint(0, width), r.randint(0, height), (0, 200, 200), 0 , 0))

	while point_list:
		if stack_mode:
			x, y, color, x0, y0 = point_list.pop()
		else:
			x, y, color, x0, y0 = point_list.popleft()
		h, s, v = color
		h = (h+1) % 180
		color = h,s,v
		
	#	if r.randint(0,47) == 0:
		#	continue
		
		direction  = r.randint(0,arc_divisor)	
		point_delta_x0 = x - x0
		point_delta_y0 = y - y0
		
		drawn = False
		attempts = 0
		
		if r.randint(0,1) == 0 and direction != arc_divisor:
			direction = -direction
		
		while not drawn:
			if direction < arc_divisor or ((x0 ==0) and (y0 == 0)):
				points = cv2.ellipse2Poly((x,y),
										  (radius, radius),
										   0,
										   direction * step_angle ,
										   direction * step_angle + step_angle ,
										   angpoints) #angle between points
			else:
				if with_straights:
					points = [[x,y], [x + point_delta_x0, y+point_delta_y0]]
				
			point_delta_x = x - points[0][0]
			point_delta_y = y - points[0][1]

			for i in points:
				i[0] += point_delta_x
				i[1] += point_delta_y

			if 0 <= points[-1][0] < width and 0 <= points[-1][1] < height: 
				if slate[points[-1][1]][points[-1][0]][2] == 0:
				
					if square_mode:
						if len(points) > 2:
							points = [points[0], points[-1]]
						
					cv2.polylines(slate, np.int32([points]) , 0, color, 1)
					
					drawn = True
			if attempts > arc_divisor:
				break
			attempts  += 1
			direction += 1
			direction %= arc_divisor 
			
		if not drawn:
			continue
		
		if r.randint(0,2) == 0:
			point_list.append((x, y, color, x0, y0 ))
		
		if (0<= points[-1][0] <= width) and (0<= points[-1][1] <= height):
		#	if h == 0 or h == 179:
		#		color = (h, s+1, v)
		#		
		#	if s %2 ==1:
		#		color = (h-2, s, v)
		#	else:
		#		color = (h+2, s, v)
			point_list.append((points[-1][0], points[-1][1], color, x, y ))
			
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