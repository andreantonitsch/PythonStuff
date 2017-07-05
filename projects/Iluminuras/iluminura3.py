import cv2
import numpy as np
import random as r
from collections import deque
import math as m


r.seed()

height = 600
width = 1200
seed_count = 3


slate = np.zeros((height,width,3), np.uint8)

color = (255, 255, 255)

# lista de pontos, x, y, vetor direcao, count
point_list = deque()
auxcount = 0

#cada ponto na grid é um dicionario de pontos para os quais o ponto pode ir
cell_width = 30
cell_height = 30
radius = 8


				
# cada ponto é uma tupla: x, y, auxcount, x0, y0
for i in range(seed_count):
	point_list.append(( r.randint(0, width), r.randint(0, height), 0, 0 , 0))

while point_list:
	x, y, count, x0, y0 = point_list.popleft()
	
	if count % 29 == 0:
		point_list.append((x, y, count+r.randint(1, 3), x0, y0 ))
	if count % 111 == 0:
		continue
		
	direction  = r.randint(0,4)	
	point_delta_x0 = x - x0
	point_delta_y0 = y - y0
	
	if direction < 4:
		points = cv2.ellipse2Poly((x,y),
								  (radius, radius),
								   0,
								   direction * 90,
								   direction * 90 + 90,
								   15) #angle between points
	else:
		points = [[x,y], [x + point_delta_x0, y+point_delta_y0]]
		
	point_delta_x = x - points[0][0]
	point_delta_y = y - points[0][1]
	
	for i in points:
		i[0] += point_delta_x
		i[1] += point_delta_y
		
		
	if (0<= points[0][0] <= width) and (0<= points[0][1] <= height):
		point_list.append((points[-1][0], points[-1][1], count+r.randint(1, 3), x, y ))
	else:
		continue

	cv2.polylines(slate, np.int32([points]) , 0, color, 1)
	
	color = ((color[0] + r.randint(0, 20)) % 256, (color[1] + r.randint(0, 20)) % 256, (color[2] + r.randint(0, 20)) % 256)
	
	if auxcount %50 ==0:
		cv2.imshow("window", slate)
		cv2.waitKey(1)
	auxcount+=1

cv2.imshow("window", slate)
cv2.waitKey(0)