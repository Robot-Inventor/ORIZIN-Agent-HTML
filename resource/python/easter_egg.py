import tkinter as tk
import random
import sys


is_started = False
ship_x = 240
ship_y = 200
rival_beam = {}
rival_beam_counter = 0
beam_speed = 400
game_over = False


BEAM_LENGTH = 20
SHIP_WIDTH = 20
SHIP_HEIGHT = 20
SHIP_COLOR = "red"
AMOUNT_OF_SHIP_MOVEMENT = 20
AMOUNT_OF_BEAM_MOVEMENT = 20
DISTANCE_BETWEEN_BEAMS = 20
TIME_REDUCTION_RATE = 2
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 300
BEAM_SPEED_REFRESH_TIME = 300
FONT_COLOR = "red"
BEAM_COLOR = "yellow"


def close_window_by_shortcut(event):
    close_window()
    return


def close_window():
    root.destroy()
    sys.exit()
    return


def space_pressed(event):
    global is_started
    if is_started is False:
        is_started = True
        game_title.destroy()
        press_space_to_start.destroy()
        game_canvas.create_rectangle(
            ship_x, ship_y, ship_x + SHIP_WIDTH, ship_y + SHIP_HEIGHT, fill=SHIP_COLOR, tag='ship'
        )
        how_to_play = tk.Label(
            game_canvas, text='矢印キーで左右へ', bg='black', fg=FONT_COLOR, font=('', 13, 'bold', 'roman', 'normal', 'normal')
        )
        how_to_play.pack(anchor=tk.NW, expand=1)
        root.after(beam_speed, beam_control)
        change_beam_speed()
        return


def move_ship(x, y):
    game_canvas.delete('ship')
    game_canvas.create_rectangle(x, y, x + SHIP_WIDTH, y + SHIP_HEIGHT, fill=SHIP_COLOR, tag='ship')
    return


def left_pressed(event):
    global ship_x
    if is_started:
        if ship_x >= SHIP_WIDTH:
            ship_x -= AMOUNT_OF_SHIP_MOVEMENT
            move_ship(ship_x, ship_y)
    return


def right_pressed(event):
    global ship_x
    if is_started:
        if ship_x <= WINDOW_WIDTH - SHIP_WIDTH * 2:
            ship_x += AMOUNT_OF_SHIP_MOVEMENT
            move_ship(ship_x, ship_y)


def beam_control():
    global rival_beam
    global rival_beam_counter
    global game_over
    if game_over:
        return
    else:
        for rival_beam_id in list(rival_beam):
            rival_beam_x = rival_beam[rival_beam_id][0]
            rival_beam_y = rival_beam[rival_beam_id][1]
            game_canvas.delete(rival_beam_id)
            game_canvas.create_line(
                rival_beam_x, rival_beam_y + BEAM_LENGTH, rival_beam_x,
                rival_beam_y + BEAM_LENGTH + AMOUNT_OF_BEAM_MOVEMENT,
                fill=BEAM_COLOR, tag=rival_beam_id
            )
            rival_beam[rival_beam_id] = [rival_beam_x, rival_beam_y + AMOUNT_OF_BEAM_MOVEMENT]
            if ship_y >= rival_beam_y >= ship_y - SHIP_HEIGHT and ship_x <= rival_beam_x <= ship_x + SHIP_WIDTH:
                game_over_message = tk.Label(
                    game_canvas, text='Game Over', bg='black', fg=FONT_COLOR,
                    font=('', 30, 'bold', 'roman', 'normal', 'normal')
                )
                game_over_message.pack(side=tk.TOP, expand=0, fill=tk.BOTH)
                game_over = True
                root.after(3000, close_window)
            if rival_beam_y >= WINDOW_HEIGHT:
                del rival_beam[rival_beam_id]
                game_canvas.delete(rival_beam_id)
        x = random.randrange(0, WINDOW_WIDTH, DISTANCE_BETWEEN_BEAMS)
        game_canvas.create_line(x, 0, x, BEAM_LENGTH, fill=BEAM_COLOR, tag=f"rival_beam{rival_beam_counter}")
        rival_beam[f"rival_beam{rival_beam_counter}"] = [x, 0]
        rival_beam_counter += 1
        root.after(beam_speed, beam_control)
        return


def change_beam_speed():
    global beam_speed
    beam_speed -= TIME_REDUCTION_RATE
    root.after(BEAM_SPEED_REFRESH_TIME, change_beam_speed)
    return


root = tk.Tk()
root.title('ORIZIN Easter Egg')
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

root.bind('<Control-q>', close_window_by_shortcut)
root.bind('<Left>', left_pressed)
root.bind('<Right>', right_pressed)
root.bind('<space>', space_pressed)

game_canvas = tk.Canvas(root, bg='black')
game_canvas.pack(anchor=tk.NW, expand=1, fill=tk.BOTH)

game_title = tk.Label(
    game_canvas, text='Space Battleship Game', bg='black', fg=FONT_COLOR,
    font=('', 30, 'bold', 'roman', 'normal', 'normal')
)
game_title.pack(expand=0, fill=tk.BOTH)
press_space_to_start = tk.Label(
    game_canvas, text='スペースキーを押してスタート', bg='black', fg=FONT_COLOR, font=('', 15, 'bold', 'roman', 'normal', 'normal')
)
press_space_to_start.pack(anchor=tk.NW, expand=1, fill=tk.BOTH)


root.mainloop()
