# -*- coding: utf8 -*-


import tkinter as tk
import time
import random
import re
import atexit
import subprocess


startMessage = True
shipX = 240
shipY = 200
rivalBeam = []
rivalBeamCount = 0
beamSpeed = 400
gameOver = 0


def shutdown(event):
    quit()


def autoShutdown():
    quit()


def spacePressed(event):
    global startMessage
    if startMessage == True:
        startMessage = False
        gameTitle.destroy()
        promptStart.destroy()
        gameCanvas.create_rectangle(shipX, shipY, shipX + 20, shipY + 20, fill='red', tag='ship')
        howToPlay = tk.Label(gameCanvas, text='矢印キーで左右へ', bg='black', fg='red', font=('', 13, 'bold', 'roman', 'normal', 'normal'))
        howToPlay.pack(anchor=tk.NW, expand=1)
        root.after(beamSpeed, moveThings)
        beamSound()
        changeBeamSpeed()


def leftPressed(event):
    global shipX
    if startMessage == False:
        if shipX >= 20:
            shipX -= 20
            gameCanvas.delete('ship')
            gameCanvas.create_rectangle(shipX, shipY, shipX + 20, shipY + 20, fill='red', tag='ship')


def rightPressed(event):
    global shipX
    if startMessage == False:
        if shipX <= 460:
            shipX += 20
            gameCanvas.delete('ship')
            gameCanvas.create_rectangle(shipX, shipY, shipX + 20, shipY + 20, fill='red', tag='ship')


def moveThings():
    global rivalBeam
    global rivalBeamCount
    rivalBeamLen = int(len(rivalBeam) / 3)
    corsor = 0
    for num in range(rivalBeamLen):
        IDPrace = corsor
        XPrace = corsor + 1
        YPrace = corsor + 2
        corsor += 3
        rivalBeamID = rivalBeam[IDPrace]
        rivalBeamX = rivalBeam[XPrace]
        rivalBeamY = rivalBeam[YPrace]
        gameCanvas.delete(rivalBeamID)
        gameCanvas.create_line(int(rivalBeamX), int(rivalBeamY) + 20, int(rivalBeamX), int(rivalBeamY) + 40, fill='yellow', tag=rivalBeamID)
        rivalBeam[YPrace] = str(int(rivalBeamY) + 20)
        if int(rivalBeam[YPrace]) <= 200 and int(rivalBeam[YPrace]) >= 180 and int(rivalBeam[XPrace]) >= shipX and int(rivalBeam[XPrace]) <= shipX + 20:
            global gameOver
            gameOver += 1
            gameOver = tk.Label(gameCanvas, text='Game Over', bg='black', fg='red', font=('', 30, 'bold', 'roman', 'normal', 'normal'))
            gameOver.pack(side=tk.TOP, expand=0, fill=tk.BOTH)
            beamSound('/home/pi/ORIZIN_Agent/sounds/soundEffects/wav/bomb1.wav')
            root.after(3000, autoShutdown)
        if int(rivalBeam[YPrace]) <= 0:
            rivalBeam.pop(0)
            rivalBeam.pop(1)
            rivalBeam.pop(2)
    X = random.randrange(0, 500, 20)
    gameCanvas.create_line(X, 0, X, 20, fill='yellow', tag='rivalBeam' + str(rivalBeamCount))
    rivalBeam.append('rivalBeam' + str(rivalBeamCount))
    rivalBeam.append(str(X))
    rivalBeam.append('0')
    rivalBeamCount += 1
    root.after(beamSpeed, moveThings)


def playSound(soundFile):
    command = 'aplay ' + soundFile
    global soundPlayer
    soundPlayer = subprocess.Popen(command.split())


def beamSound(soundFile='/home/pi/ORIZIN_Agent/sounds/soundEffects/wav/laser1.wav'):
    command = 'aplay ' + soundFile
    subprocess.Popen(command.split())
    root.after(1000, beamSound)


def stopSound():
    soundPlayer.terminate()


def changeBeamSpeed():
    global beamSpeed
    beamSpeed -= 2
    root.after(300, changeBeamSpeed)


atexit.register(stopSound)


root = tk.Tk()
root.title('ORIZIN Easter Egg')
root.geometry("500x300")

root.bind('<Control-q>', shutdown)
root.bind('<Left>', leftPressed)
root.bind('<Right>', rightPressed)
root.bind('<space>', spacePressed)

playSound('/home/pi/ORIZIN_Agent/sounds/musics/wav/natsuhasummer.wav')

gameCanvas = tk.Canvas(root, bg='black')
gameCanvas.pack(anchor=tk.NW, expand=1, fill=tk.BOTH)

gameTitle = tk.Label(gameCanvas, text='Space Battleship Game', bg='black', fg='red', font=('', 30, 'bold', 'roman', 'normal', 'normal'))
gameTitle.pack(expand=0, fill=tk.BOTH)
promptStart = tk.Label(gameCanvas, text='スペースキーを押してスタート', bg='black', fg='red', font=('', 15, 'bold', 'roman', 'normal', 'normal'))
promptStart.pack(anchor=tk.NW, expand=1, fill=tk.BOTH)


root.mainloop()
