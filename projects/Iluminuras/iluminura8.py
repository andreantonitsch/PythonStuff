import cv2
import numpy as np
import random as r
from collections import deque
import math as m


###
### versao STACK
###
while True:
	r.seed()

	height = 600
	width = 1200
	seed_count = 3
	
	square_mode = False

	slate = np.zeros((height,width,3), np.uint8)


	#color = (255, 255, 255)

	# lista de pontos, x, y, vetor direcao, count
	point_list = deque()
	auxcount = 0

	#cada ponto na grid é um dicionario de pontos para os quais o ponto pode ir
	cell_width = 30
	cell_height = 30
	radius = 8
	angpoints = 10
	
	color = (0, 200, 200)
	color_up = False
	
	# cada ponto é uma tupla: x, y, colorHSV, x0, y0
	for i in range(seed_count):
		point_list.append(( r.randint(0, height), r.randint(0, width), 0 , 0))

	while point_list:
		x, y, x0, y0 = point_list.pop()

		if r.randint(0,2) == 0:
			point_list.append((x, y, x0, y0 ))
	#	if r.randint(0,47) == 0:
		#	continue
		
		direction  = r.randint(0,4)	
		point_delta_x0 = x - x0
		point_delta_y0 = y - y0
		
		drawn = False
		attempts = 0
		while not drawn:
			if direction < 4 or ((x0 ==0) and (y0 == 0)):
				points = cv2.ellipse2Poly((x,y),
										  (radius, radius),
										   0,
										   direction * 90 ,
										   direction * 90 + 90 ,
										   angpoints) #angle between points
			else:
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
					
					h, s, v = color
					if h == 179 or h == 0:
						color_up = not color_up
					if color_up:
						color = (h+1, s, v)
					else:
						color = (h-1, s, v)
	
					cv2.polylines(slate, np.int32([points]) , 0, color, 1)
					
					drawn = True
			if attempts > 5:
				break
			attempts += 1
			direction+=1 % 5
		if not drawn:
			continue
					
		if (0<= points[-1][0] <= width) and (0<= points[-1][1] <= height):
			point_list.append((points[-1][0], points[-1][1], x, y ))
			
		else:
			continue
		
		print(len(point_list))
		
		if auxcount % 20 == 0:
			hsv = cv2.cvtColor(slate, cv2.COLOR_HSV2BGR)
			cv2.imshow("window", hsv)
			cv2.waitKey(1)
		auxcount+=1

hsv = cv2.cvtColor(slate, cv2.COLOR_HSV2BGR)
cv2.imshow("window", hsv)
cv2.waitKey(0)