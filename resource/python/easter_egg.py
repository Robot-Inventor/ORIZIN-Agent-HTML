import tkinter as tk
import random
import sys


startMessage = True
shipX = 240
shipY = 200
rivalBeam = []
rivalBeamCount = 0
beamSpeed = 400


def shutdown(event):
    root.destroy()
    sys.exit()


def auto_shutdown():
    root.destroy()
    sys.exit()


def space_pressed(event):
    global startMessage
    if startMessage:
        startMessage = False
        gameTitle.destroy()
        promptStart.destroy()
        gameCanvas.create_rectangle(shipX, shipY, shipX + 20, shipY + 20, fill='red', tag='ship')
        how_to_play = tk.Label(
            gameCanvas, text='矢印キーで左右へ', bg='black', fg='red', font=('', 13, 'bold', 'roman', 'normal', 'normal')
        )
        how_to_play.pack(anchor=tk.NW, expand=1)
        root.after(beamSpeed, move_things)
        change_beam_speed()


def left_pressed(event):
    global shipX
    if startMessage is False:
        if shipX >= 20:
            shipX -= 20
            gameCanvas.delete('ship')
            gameCanvas.create_rectangle(shipX, shipY, shipX + 20, shipY + 20, fill='red', tag='ship')


def right_pressed(event):
    global shipX
    if startMessage is False:
        if shipX <= 460:
            shipX += 20
            gameCanvas.delete('ship')
            gameCanvas.create_rectangle(shipX, shipY, shipX + 20, shipY + 20, fill='red', tag='ship')


def move_things():
    global rivalBeam
    global rivalBeamCount
    rival_beam_len = int(len(rivalBeam) / 3)
    cursor = 0
    for num in range(rival_beam_len):
        id_place = cursor
        x_place = cursor + 1
        y_place = cursor + 2
        cursor += 3
        rival_beam_id = rivalBeam[id_place]
        rival_beam_x = rivalBeam[x_place]
        rival_beam_y = rivalBeam[y_place]
        gameCanvas.delete(rival_beam_id)
        gameCanvas.create_line(
            int(rival_beam_x), int(rival_beam_y) + 20, int(rival_beam_x), int(rival_beam_y) + 40,
            fill='yellow', tag=rival_beam_id
        )
        rivalBeam[y_place] = str(int(rival_beam_y) + 20)
        if 200 >= int(rivalBeam[y_place]) >= 180 and shipX <= int(rivalBeam[x_place]) <= shipX + 20:
            game_over = tk.Label(
                gameCanvas, text='Game Over', bg='black', fg='red', font=('', 30, 'bold', 'roman', 'normal', 'normal')
            )
            game_over.pack(side=tk.TOP, expand=0, fill=tk.BOTH)
            root.after(3000, auto_shutdown)
        if int(rivalBeam[y_place]) <= 0:
            rivalBeam.pop(0)
            rivalBeam.pop(1)
            rivalBeam.pop(2)
    x = random.randrange(0, 500, 20)
    gameCanvas.create_line(x, 0, x, 20, fill='yellow', tag='rivalBeam' + str(rivalBeamCount))
    rivalBeam.append('rivalBeam' + str(rivalBeamCount))
    rivalBeam.append(str(x))
    rivalBeam.append('0')
    rivalBeamCount += 1
    root.after(beamSpeed, move_things)


def change_beam_speed():
    global beamSpeed
    beamSpeed -= 2
    root.after(300, change_beam_speed)


root = tk.Tk()
root.title('ORIZIN Easter Egg')
root.geometry("500x300")

root.bind('<Control-q>', shutdown)
root.bind('<Left>', left_pressed)
root.bind('<Right>', right_pressed)
root.bind('<space>', space_pressed)

gameCanvas = tk.Canvas(root, bg='black')
gameCanvas.pack(anchor=tk.NW, expand=1, fill=tk.BOTH)

gameTitle = tk.Label(
    gameCanvas, text='Space Battleship Game', bg='black', fg='red', font=('', 30, 'bold', 'roman', 'normal', 'normal')
)
gameTitle.pack(expand=0, fill=tk.BOTH)
promptStart = tk.Label(
    gameCanvas, text='スペースキーを押してスタート', bg='black', fg='red', font=('', 15, 'bold', 'roman', 'normal', 'normal')
)
promptStart.pack(anchor=tk.NW, expand=1, fill=tk.BOTH)


root.mainloop()
