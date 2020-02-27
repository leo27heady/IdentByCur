import tkinter
from tkinter import *
import random
from pynput import mouse
import time
import pickle
import copy
import math
import threading

import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier


# data = []  # ["Class", x, y, time.0]
full_list = []
frame_data = []
btnCounter = 0
fileI = 0
pos = None
expertMode = False

# Person Parmtrs
whois = int(1)  # !!!!!!!!!!!!!!
fileName = "LeoSunday12Re_{0}_5.pickle"

def maxloop(index, my_list, full_lenth):
    num = 1
    indx = 0
    lenthelx = 0
    lenthx = 0
    maX = 0
    for k in range(1, len(my_list)):
        lenthelx = math.sqrt((my_list[k][1] - my_list[k - 1][1]) ** 2 + (my_list[k][2] - my_list[k - 1][2]) ** 2)
        lenthx += lenthelx
        if lenthx >= full_lenth / index or (num == index and k == (len(my_list) - 1)):
            num += 1
            speed = lenthx / (my_list[k][3] - my_list[indx][3])
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
            lentheli = math.sqrt(
                (full_list[i][j][1] - full_list[i][j - 1][1]) ** 2 + (full_list[i][j][2] - full_list[i][j - 1][2]) ** 2)
            lenthi += lentheli

        speedi = lenthi / (full_list[i][-1][3] - full_list[i][0][3])

        # FIRST SPEED AND FIRST LENTH
        lenthk = 0
        for k in range(1, len(full_list[i])):
            lenthelk = math.sqrt(
                (full_list[i][k][1] - full_list[i][k - 1][1]) ** 2 + (full_list[i][k][2] - full_list[i][k - 1][2]) ** 2)
            lenthk += lenthelk
            if lenthk >= lenthi / 10:
                fssi = lenthk / (full_list[i][k][3] - full_list[i][0][3])
                firstSpeed.append(fssi)
                firstLenth.append(lenthk)
                break

        # MAX SPEED
        if len(full_list[i]) < 20:
            maxsi = speedi
        elif len(full_list[i]) < 50:
            maxsi = maxloop(3, full_list[i], lenthi)
        else:
            maxsi = maxloop(len(full_list[i]) // 10, full_list[i], lenthi)
        if maxsi < speedi or maxsi < fssi:
            if fssi > speedi:
                maxsi = fssi
            else:
                maxsi = speedi

        # DEVIATION

        # Ax + By + C = 0
        A = full_list[i][0][2] - full_list[i][-1][2]  # A = y1 - y2
        B = full_list[i][-1][1] - full_list[i][0][1]  # B = x2 - x1
        C = (full_list[i][0][1] * full_list[i][-1][2]) - (full_list[i][-1][1] * full_list[i][0][2])  # C = x1*y2 - x2*y1

        pointToLine = []  # distance
        disAver = 0
        for d in range(len(full_list[i])):
            dis = abs(A * full_list[i][d][1] + B * full_list[i][d][2] + C) / math.sqrt(A ** 2 + B ** 2)
            pointToLine.append(dis)  # distance = |A*x0 + B*y0 + C| / _/-(A^2 + B^2)
            disAver += dis
        disAver /= len(full_list[i])  # average distance

        subD = 0
        for x in range(len(full_list[i])): subD += (pointToLine[x] - disAver) ** 2

        time.append(full_list[i][-1][3] - full_list[i][0][3])  # previous
        fullLenth.append(lenthi)
        averSpeed.append(speedi)
        maxSpeed.append(maxsi)
        clickWait.append(full_list[i][-1][3] - full_list[i][-2][3])  # ))))0
        deviation.append(math.sqrt(subD / len(full_list[i])))  # deviation = _/- ( (E (di - dd)^2)) / n )

    whoisList = []
    pList = []
    for i in range(len(full_list)):
        parli = [time[i], fullLenth[i], averSpeed[i], firstSpeed[i], firstLenth[i], maxSpeed[i], clickWait[i],
                 deviation[i]]
        pList.append(parli)
        whoisList.append(whois)

    paramList = [pList, whoisList]
    return paramList


def cut():
    global frame_data

    if len(frame_data) < 2: return True  # double click protect
    if frame_data[-1][3] - frame_data[0][3] < 0.2: return True  # fast move protect

    for x in reversed(range(1, len(frame_data))):  # [j, j - 1, j - 2, ... , 0]
        if frame_data[x][3] - frame_data[x - 1][3] >= 1.0:  # if stop time more then 1 sec
            return True

    return False


def on_move(x, y):
    global frame_data

    data = ["move", int(x), int(y), float(time.time())]
    frame_data.append(data)


def on_click(x, y, button, pressed):
    global full_list
    global frame_data
    global btnCounter
    global pos

    if pressed:
        if 0 <= int(x) - pos[0] <= 86 and 0 <= int(y) - pos[1] <= 85:
            data = ["click", int(x), int(y), float(time.time())]
            frame_data.append(data)
            if not cut():
                full_list.append(copy.deepcopy(frame_data))
                btnCounter += 1
            frame_data = []

            if btnCounter == 10:
                mouse.Listener.stop()


def randPosition():
    return [random.randint(0, 1194), random.randint(0, 715)]


def thread_function(name):
    with mouse.Listener(on_move=on_move, on_click=on_click) as Listener:
        Listener.join()


def moveButton():
    global pos
    btn.place_forget()

    btnGBC.place_forget()
    btnETC.place_forget()
    btnRFC.place_forget()
    btnDTC.place_forget()
    btnKNC.place_forget()
    btnLR.place_forget()
    btnNNA.place_forget()
    # btnNN.place_forget()

    btn.configure(text="     ",
                  font=('calibri', 30, 'bold'),
                  command=jumpButton,
                  highlightbackground="#ff003c")
    x = threading.Thread(target=thread_function, args=(1,))
    x.start()

    pos = randPosition()
    btn.place(x=pos[0], y=pos[1])


def jumpButton():
    global btnCounter
    global full_list
    global frame_data
    global btnCounter
    global fileI
    global pos

    if btnCounter == 10:
        tcpList = param()

        pr_mlp = 0
        pr_lr = 0
        pr_knn = 0
        pr_dtc = 0
        pr_rfc = 0
        pr_etc = 0
        pr_gbc = 0

        if expertMode:
            pickle_out = open(fileName.format(fileI), "wb")  # !!!!!!!!!!!!!!
            pickle.dump(tcpList, pickle_out)
            pickle_out.close()
            print(tcpList)
        else:
            print(tcpList)
            pickle_in = open("weights/fit_transform_prmtrs.pickle", "rb")
            fit_transform = pickle.load(pickle_in)
            transformedTCP = []
            for i in tcpList[0]:
                trans_i = []
                for j in range(len(fit_transform)):
                    if i[j] <= fit_transform[j][2]:
                        i[j] = fit_transform[j][2]
                    elif i[j] >= fit_transform[j][3]:
                        i[j] = fit_transform[j][3]
                    trans_i.append((i[j] - fit_transform[j][0])/fit_transform[j][1])
                transformedTCP.append(trans_i)

            transformedTCP = np.array(transformedTCP)

            pickle_in = open("weights/NeuralNetworAutoWeight.pickle", "rb")
            mlp = pickle.load(pickle_in)
            predict_mlp = mlp.predict(transformedTCP)
            print(predict_mlp)
            pr_mlp = int(predict_mlp.sum()/len(predict_mlp)*100)

            pickle_in = open("weights/LogisticRegressionWeight.pickle", "rb")
            logreg = pickle.load(pickle_in)
            predict_lr = logreg.predict(transformedTCP)
            print(predict_lr)
            pr_lr = int(predict_lr.sum()/len(predict_lr)*100)

            pickle_in = open("weights/KNeighborsWeight.pickle", "rb")
            knn = pickle.load(pickle_in)
            predict_knn = knn.predict(transformedTCP)
            print(predict_knn)
            pr_knn = int(predict_knn.sum()/len(predict_knn)*100)

            pickle_in = open("weights/DecisionTreeWeight.pickle", "rb")
            dtc = pickle.load(pickle_in)
            predict_dtc = dtc.predict(transformedTCP)
            print(predict_dtc)
            pr_dtc = int(predict_dtc.sum()/len(predict_dtc)*100)

            pickle_in = open("weights/RandomForestWeight.pickle", "rb")
            rfc = pickle.load(pickle_in)
            predict_rfc = rfc.predict(transformedTCP)
            print(predict_rfc)
            pr_rfc = int(predict_rfc.sum()/len(predict_rfc)*100)

            pickle_in = open("weights/ExtraTreesWeight.pickle", "rb")
            etc = pickle.load(pickle_in)
            predict_etc = etc.predict(transformedTCP)
            print(predict_etc)
            pr_etc = int(predict_etc.sum()/len(predict_etc)*100)

            pickle_in = open("weights/GradientBoostingWeight.pickle", "rb")
            gbc = pickle.load(pickle_in)
            predict_gbc = gbc.predict(transformedTCP)
            print(predict_gbc)
            pr_gbc = int(predict_gbc.sum()/len(predict_gbc)*100)


        full_list = []
        frame_data = []
        btnCounter = 0
        fileI += 1

        btnNNA.configure(
            text="NNA\n{0}%".format(pr_mlp),
            highlightbackground = "#32a852" if pr_mlp > 50 else "#e33333",
            fg = "#32a852" if pr_mlp > 50 else "#e33333"
        )
        btnNNA.place(relx=0.386, rely=0.024, anchor=CENTER)

        btnLR.configure(
            text="LR\n{0}%".format(pr_lr),
            highlightbackground = "#32a852" if pr_lr > 50 else "#e33333",
            fg = "#32a852" if pr_lr > 50 else "#e33333"
        )
        btnLR.place(relx=0.424, rely=0.024, anchor=CENTER)

        btnKNC.configure(
            text="KNC\n{0}%".format(pr_knn),
            highlightbackground = "#32a852" if pr_knn > 50 else "#e33333",
            fg = "#32a852" if pr_knn > 50 else "#e33333"
        )
        btnKNC.place(relx=0.462, rely=0.024, anchor=CENTER)

        btnDTC.configure(
            text="DTC\n{0}%".format(pr_dtc),
            highlightbackground = "#32a852" if pr_dtc > 50 else "#e33333",
            fg = "#32a852" if pr_dtc > 50 else "#e33333"
        )
        btnDTC.place(relx=0.500, rely=0.024, anchor=CENTER)

        btnRFC.configure(
            text="RFC\n{0}%".format(pr_rfc),
            highlightbackground = "#32a852" if pr_rfc > 50 else "#e33333",
            fg = "#32a852" if pr_rfc > 50 else "#e33333"
        )
        btnRFC.place(relx=0.538, rely=0.024, anchor=CENTER)

        btnETC.configure(
            text="ETC\n{0}%".format(pr_etc),
            highlightbackground = "#32a852" if pr_etc > 50 else "#e33333",
            fg = "#32a852" if pr_etc > 50 else "#e33333"
        )
        btnETC.place(relx=0.576, rely=0.024, anchor=CENTER)

        btnGBC.configure(
            text="GBC\n{0}%".format(pr_gbc),
            highlightbackground = "#32a852" if pr_gbc > 50 else "#e33333",
            fg = "#32a852" if pr_gbc > 50 else "#e33333"
        )
        btnGBC.place(relx=0.614, rely=0.024, anchor=CENTER)


        btn.place_forget()
        btn.configure(
            font=('calibri', 32, 'bold'),
            highlightbackground="#8800ff",
            fg="#8800ff",
            highlightthickness=0,
            command=moveButton,
            text="Let's move!",
            borderwidth='0'
        )
        btn.place(relx=0.5, rely=0.5, anchor=CENTER)

        return

    btn.place_forget()
    btn.configure(text="     ",
                  font=('calibri', 30, 'bold'),
                  command=jumpButton,
                  highlightbackground="#ff003c")

    pos = randPosition()
    btn.place(x=pos[0], y=pos[1])


root = tkinter.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("{0}x{1}".format(screen_width, screen_height))

root.title("Mouse Identy")

root.configure(background='#690eb3')

btn = Button(
    root,
    font=('calibri', 32, 'bold'),
    highlightbackground="#8800ff",
    fg="#8800ff",
    highlightthickness=0,
    command=moveButton,
    text="Let's move!",
    borderwidth='0'
)
btn.place(relx=0.5, rely=0.5, anchor=CENTER)


def createButton(text):
    button = Button(
        root,
        font=('calibri', 12, 'bold'),
        highlightbackground="#e33333",
        fg="#e33333",
        highlightthickness=0,
        text=text,
        borderwidth='0',
        height=2,
        width=5
    )
    return button


btnNNA = createButton("NNA\n0.0%")
btnNNA.place(relx=0.386, rely=0.024, anchor=CENTER)

btnLR = createButton("LR\n0.0%")
btnLR.place(relx=0.424, rely=0.024, anchor=CENTER)

btnKNC = createButton("KNC\n0.0%")
btnKNC.place(relx=0.462, rely=0.024, anchor=CENTER)

btnDTC = createButton("DTC\n0.0%")
btnDTC.place(relx=0.500, rely=0.024, anchor=CENTER)

btnRFC = createButton("RFC\n0.0%")
btnRFC.place(relx=0.538, rely=0.024, anchor=CENTER)

btnETC = createButton("ETC\n0.0%")
btnETC.place(relx=0.576, rely=0.024, anchor=CENTER)

btnGBC = createButton("GBC\n0.0%")
btnGBC.place(relx=0.614, rely=0.024, anchor=CENTER)

root.mainloop()
