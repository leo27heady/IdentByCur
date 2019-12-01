from pynput import mouse
import time
import pickle
import copy
import math

full_list = []
data = [] # ["Class", x, y, time.0]
frame_data = []

def cut():
	for i in range(len(full_list)):
		try:
			if len(full_list[i]) < 2:
				full_list.pop(i)
				i -= 1  
				continue
		except IndexError as e:
			break

		if full_list[i][-1][3] - full_list[i][0][3] > 2.0: # if move time more then 2 sec
			for x in reversed(range(1, len(full_list[i]))): # [j, j - 1, j - 2, ... , 0]
				if full_list[i][x][3] - full_list[i][x - 1][3] >= 1.0: # if stop time more then 1 sec
					if x + 8 < len(full_list[i]): # if it isnt last el
						full_list[i] = copy.deepcopy(full_list[i][x:]) # remove all until stop time..
						break    

def maxloop(index, my_list, full_lenth):
	num = 1
	indx = 0
	lenthelx = 0
	lenthx = 0
	maX = 0
	for k in range(1, len(my_list)):
		lenthelx = math.sqrt((my_list[k][1] - my_list[k - 1][1])**2 + (my_list[k][2] - my_list[k - 1][2])**2) 
		lenthx += lenthelx
		if lenthx >= full_lenth/index or (num == index and k == (len(my_list) - 1)):
			num += 1
			speed = lenthx/(my_list[k][3] - my_list[indx][3])
			if speed > maX: 
				maX = speed
			indx = k
			lenthx = 0
	return maX

def param():

	time = []
	fullLenth = []
	firstLenth = []
	averSpeed = []
	firstSpeed = []
	maxSpeed = []
	clickWait = []
	deviation = []

	for i in range(len(full_list)):
			
		
		lenthi = 0
		speedi = 0
		maxsi = 0
		fssi = 0
		for j in range(1, len(full_list[i])):
			# lenthi - its i elmnt of fullLenth = E(i...n)_/-( (Xi - Xi-1)^2 + (Yi - Yi-1)^2 )
			lentheli = math.sqrt((full_list[i][j][1] - full_list[i][j - 1][1])**2 + (full_list[i][j][2] - full_list[i][j - 1][2])**2) 
			lenthi += lentheli

		speedi = lenthi/(full_list[i][-1][3] - full_list[i][0][3])


		# FIRST SPEED AND FIRST LENTH
		lenthk = 0
		for k in range(1, len(full_list[i])):
			lenthelk = math.sqrt((full_list[i][k][1] - full_list[i][k - 1][1])**2 + (full_list[i][k][2] - full_list[i][k - 1][2])**2) 
			lenthk += lenthelk
			if lenthk >= lenthi/10:
				fssi = lenthk/(full_list[i][k][3] - full_list[i][0][3])
				firstSpeed.append(fssi)
				firstLenth.append(lenthk)
				break

		# MAX SPEED
		if len(full_list[i]) < 20:
			maxsi = speedi
		elif len(full_list[i]) < 50:
			maxsi = maxloop(3, full_list[i], lenthi)
		elif len(full_list[i]) < 100:
			maxsi = maxloop(10, full_list[i], lenthi)
		elif len(full_list[i]) < 500:
			maxsi = maxloop(20, full_list[i], lenthi)
		else:
			maxsi = maxloop(100, full_list[i], lenthi)
		if maxsi < speedi or maxsi < fssi:
			if fssi > speedi:
				maxsi = fssi
			else:
				maxsi = speedi

		# DEVIATION

		# Ax + By + C = 0
		A = full_list[i][0][2] - full_list[i][-1][2] # A = y1 - y2
		B = full_list[i][-1][1] - full_list[i][0][1] # B = x2 - x1
		C = full_list[i][0][1]*full_list[i][-1][2] - full_list[i][-1][1]*full_list[i][0][2] # C = x1*y2 - x2*y1

		pointToLine = [] # distance
		disAver = 0
		for d in range(len(full_list[i])):
			dis = abs(A*full_list[i][d][1] + B*full_list[i][d][2] + C)/math.sqrt(A**2 + B**2)
			pointToLine.append(dis) # distance = |A*x0 + B*y0 + C| / _/-(A^2 + B^2)
			disAver += dis 
		disAver /= len(full_list[i]) # average distance

		subD = 0
		for x in range(len(full_list[i])): subD += (pointToLine[x] - disAver)**2


		time.append(full_list[i][-1][3] - full_list[i][0][3]) # previous
		fullLenth.append(lenthi)
		averSpeed.append(speedi)
		maxSpeed.append(maxsi)
		clickWait.append(full_list[i][-1][3] - full_list[i][-2][3]) # ))))0
		deviation.append(math.sqrt(subD/len(full_list[i]))) # deviation = _/- ( (E (di - dd)^2)) / n )

	whoisList = []
	pList = []
	for i in range(len(full_list)):
		parli = [time[i], fullLenth[i], averSpeed[i], firstSpeed[i], firstLenth[i], maxSpeed[i], clickWait[i], deviation[i]]
		whois = int(1)
		pList.append(parli)
		whoisList.append(whois)

	paramList = [pList, whoisList]
	return paramList

def on_move(x, y):
	global frame_data

	data = ["move", int(x), int(y), float(time.time())]
	frame_data.append(data)
	print(data)

def on_click(x, y, button, pressed):
	global full_list
	global frame_data

	if pressed:
		if x < 2 and y < 2: # seriallization
			cut()
			tcpList = param()
			pickle_out = open("tcp.pickle", "wb")
			pickle.dump(tcpList, pickle_out)
			pickle_out.close()
			print(tcpList)
			raise SystemExit
		else:
			data=["click", int(x), int(y), float(time.time())]
			
			frame_data.append(data)
			full_list.append(copy.deepcopy(frame_data))
			print(full_list)
		frame_data = []

with mouse.Listener(on_move=on_move, on_click=on_click) as Listener:
	Listener.join()