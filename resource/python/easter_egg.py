import tkinter as tk
import random
import sys


BEAM_LENGTH = 20
SHIP_WIDTH = 20
SHIP_HEIGHT = 20
SHIP_COLOR = "red"
DEFAULT_AMOUNT_OF_SHIP_MOVEMENT = 20
AMOUNT_OF_BEAM_MOVEMENT = 20
DISTANCE_BETWEEN_BEAMS = 20
DEFAULT_BEAM_SPEED = 400
BEAM_SPEED_REFRESH_TIME = 500
TIME_REDUCTION_RATE = 0.007
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 300
FONT_COLOR = "red"
BEAM_COLOR = "yellow"


is_started = False
ship_x = 240
ship_y = 200
rival_beam = {}
rival_beam_counter = 0
beam_speed = DEFAULT_BEAM_SPEED
game_over = False
amount_of_ship_movement = DEFAULT_AMOUNT_OF_SHIP_MOVEMENT
is_slow_mode = False
is_fast_mode = False
is_god_mode = False
score = 0


def close_window_by_shortcut(event):
    close_window()
    return


def close_window():
    root.destroy()
    sys.exit()
    return


def start_game(event):
    global is_started
    global score_text
    global game_over
    global score
    global beam_speed
    global is_god_mode
    if is_started is False:
        is_started = True
        game_over = False
        is_god_mode = False
        score = 0
        beam_speed = DEFAULT_BEAM_SPEED
        for rival_beam_id in list(rival_beam):
            del rival_beam[rival_beam_id]
            game_canvas.delete(rival_beam_id)
        game_title.destroy()
        game_over_message.destroy()
        game_clear_message.destroy()
        press_space_to_start.destroy()
        game_canvas.create_rectangle(
            ship_x, ship_y, ship_x + SHIP_WIDTH, ship_y + SHIP_HEIGHT, fill=SHIP_COLOR, tag='ship'
        )
        how_to_play = tk.Label(
            game_canvas, text='矢印キーで左右へ', bg='black', fg=FONT_COLOR, font=('', 13, 'bold', 'roman', 'normal', 'normal')
        )
        how_to_play.place(x=0, y=0, relwidth=1)
        score_text = tk.StringVar()
        score_text.set(str(score))
        score_label = tk.Label(
            root, textvariable=score_text, bg='black', fg=FONT_COLOR,
            font=('', 13, 'bold', 'roman', 'normal', 'normal'), anchor="e"
        )
        score_label.place(x=0, y=20, relwidth=1)
        root.after(beam_speed, beam_control)
        change_beam_speed()
        return


def move_ship(x, y):
    game_canvas.delete('ship')
    game_canvas.create_rectangle(x, y, x + SHIP_WIDTH, y + SHIP_HEIGHT, fill=SHIP_COLOR, tag='ship')
    return


def move_ship_to_left(event):
    global ship_x
    if is_started:
        ship_x -= amount_of_ship_movement
        ship_x = min(max(ship_x, 0), WINDOW_WIDTH - SHIP_WIDTH)
        move_ship(ship_x, ship_y)
    return


def move_ship_to_right(event):
    global ship_x
    if is_started:
        ship_x += amount_of_ship_movement
        ship_x = min(max(ship_x, 0), WINDOW_WIDTH - SHIP_WIDTH)
        move_ship(ship_x, ship_y)


def window_resize_watcher():
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    global ship_y
    global ship_x
    global BEAM_LENGTH
    window_width_new = root.winfo_width()
    window_height_new = root.winfo_height()
    is_window_resized = False
    if WINDOW_WIDTH != window_width_new and window_height_new != 1:
        WINDOW_WIDTH = root.winfo_width()
        if ship_x > WINDOW_WIDTH:
            ship_x = WINDOW_WIDTH - SHIP_WIDTH
        is_window_resized = True
    if WINDOW_HEIGHT != window_height_new and window_height_new != 1:
        WINDOW_HEIGHT = root.winfo_height()
        ship_y = int(WINDOW_HEIGHT - WINDOW_HEIGHT / 5)
        is_window_resized = True
    if is_window_resized:
        move_ship(ship_x, ship_y)
    root.after(1000, window_resize_watcher)
    return


def enable_slow_mode(event):
    global amount_of_ship_movement
    global is_slow_mode
    amount_of_ship_movement = DEFAULT_AMOUNT_OF_SHIP_MOVEMENT * 0.5
    is_slow_mode = True
    return


def disable_slow_mode(event):
    global amount_of_ship_movement
    global is_slow_mode
    amount_of_ship_movement = DEFAULT_AMOUNT_OF_SHIP_MOVEMENT
    is_slow_mode = False
    return


def enable_fast_mode(event):
    global amount_of_ship_movement
    global is_fast_mode
    amount_of_ship_movement = DEFAULT_AMOUNT_OF_SHIP_MOVEMENT * 2
    is_fast_mode = True
    return


def disable_fast_mode(event):
    global amount_of_ship_movement
    global is_fast_mode
    amount_of_ship_movement = DEFAULT_AMOUNT_OF_SHIP_MOVEMENT
    is_fast_mode = False
    return


def enable_god_mode(event):
    global is_god_mode
    is_god_mode = True
    return


def beam_control():
    global rival_beam
    global rival_beam_counter
    global game_over
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    global score
    global is_started
    global game_over_message
    global game_clear_message
    global ship_x
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
            if is_god_mode:
                while ship_y >= rival_beam_y >= ship_y - SHIP_HEIGHT and \
                        ship_x <= rival_beam_x <= ship_x + SHIP_WIDTH:
                    ship_x = random.randrange(
                        max(ship_x - SHIP_WIDTH * 4, 0), min(ship_x + SHIP_WIDTH * 4, WINDOW_WIDTH - SHIP_WIDTH))
                    move_ship(ship_x, ship_y)
            else:
                if ship_y >= rival_beam_y >= ship_y - SHIP_HEIGHT and ship_x <= rival_beam_x <= ship_x + SHIP_WIDTH:
                    game_over_message = tk.Label(
                        game_canvas, text=f'Game Over\nScore: {score}\nスペースキーでリトライ', bg='black', fg=FONT_COLOR,
                        font=('', 30, 'bold', 'roman', 'normal', 'normal')
                    )
                    game_over_message.place(x=0, y=0, relwidth=1, relheight=1)
                    game_over = True
                    is_started = False
            if rival_beam_y >= WINDOW_HEIGHT or rival_beam_x > WINDOW_WIDTH:
                del rival_beam[rival_beam_id]
                game_canvas.delete(rival_beam_id)
                score += 1
                score_text.set(score)
            if score >= 10000:
                game_clear_message = tk.Label(
                    game_canvas, text='Game Clear\nスペースキーでもう1度', bg='black', fg=FONT_COLOR,
                    font=('', 30, 'bold', 'roman', 'normal', 'normal')
                )
                game_clear_message.place(x=0, y=0, relwidth=1, relheight=1)
                game_over = True
                is_started = False
        x = random.randrange(DISTANCE_BETWEEN_BEAMS, WINDOW_WIDTH, DISTANCE_BETWEEN_BEAMS)
        if x == WINDOW_WIDTH:
            x -= 2
        game_canvas.create_line(x, 0, x, BEAM_LENGTH, fill=BEAM_COLOR, tag=f"rival_beam{rival_beam_counter}")
        rival_beam[f"rival_beam{rival_beam_counter}"] = [x, 0]
        rival_beam_counter += 1
        root.after(beam_speed, beam_control)
        return


def change_beam_speed():
    global beam_speed
    if not game_over:
        beam_speed = max(int(beam_speed * (1 - TIME_REDUCTION_RATE)), 5)
        root.after(BEAM_SPEED_REFRESH_TIME, change_beam_speed)
    return


root = tk.Tk()
root.title('ORIZIN Easter Egg')
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

root.bind('<Control-q>', close_window_by_shortcut)
root.bind('<Left>', move_ship_to_left)
root.bind('<Right>', move_ship_to_right)
root.bind('<space>', start_game)
root.bind("s", enable_slow_mode)
root.bind("<KeyRelease-s>", disable_slow_mode)
root.bind("f", enable_fast_mode)
root.bind("<KeyRelease-f>", disable_fast_mode)
root.bind("<Control-g>", enable_god_mode)

game_canvas = tk.Canvas(root, bg='black')
game_canvas.place(x=0, y=0, relwidth=1, relheight=1)
press_space_to_start = tk.Label(
    game_canvas, text='スペースキーを押してスタート', bg='black', fg=FONT_COLOR, font=('', 15, 'bold', 'roman', 'normal', 'normal')
)
press_space_to_start.place(x=0, y=0, relwidth=1, relheight=1)
game_title = tk.Label(
    game_canvas, text='Space Battleship Game', bg='black', fg=FONT_COLOR,
    font=('', 30, 'bold', 'roman', 'normal', 'normal')
)
game_title.place(x=0, y=0, relwidth=1)
score_text = tk.StringVar()
game_over_message = tk.Label()
game_clear_message = tk.Label()
score_text.set(0)
window_resize_watcher()

root.mainloop()
