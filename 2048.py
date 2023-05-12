import json
from tkinter import *
import random
import os
import math
from PIL import Image, ImageTk

game = Tk()
game.title("2048")
game.geometry("610x760+400+30")
background_color = '#a0968c'
colors = [('#cdbeb4', 'black'), ('#ebe1d7', 'black'), ('#f0e1c8', 'black'), ('#f0af78', 'white')
    , ('#fa9664', 'white'), ('#fa7d5f', 'white'), ('#fa643c', 'white'), ('#f0d273', 'white'), ('#f0c864', 'white')
    , ('#f0c850', 'white'), ('#f0c83c', 'white'), ('#f0be28', 'white'), ('black', 'white')]
up_frame = Frame(game, width=610, height=150)
up_frame.grid(row=0, column=0)
up_frame.grid_propagate(False)

frame2 = Frame(game, bg=background_color, padx=5, pady=5)
frame2.grid(row=1, column=0)

title = Label(up_frame, text="2048", font="Times 50 bold", padx=5)
result = Label(up_frame, text="", font="Times 30 bold", fg="green")

score = 0
high_score = 0
score_frame1 = Frame(up_frame, bg=background_color)
score_frame1.grid(row=0, column=1, padx=(140, 30))
score_name = Label(score_frame1, text="Score: ", font="Times 15 bold", padx=5, bg=background_color)
score_val = Label(score_frame1, text=str(score), font="Times 15 bold", padx=5, bg=background_color)

score_frame2 = Frame(up_frame, bg=background_color)
score_frame2.grid(row=0, column=2)
high_score_name = Label(score_frame2, text="High Score: ", font="Times 15 bold", padx=5, bg=background_color)
high_score_val = Label(score_frame2, text=str(high_score), font="Times 15 bold", padx=5, bg=background_color)
image1 = Image.open('undo.png')
res1 = image1.resize((25, 25))
undo_img = ImageTk.PhotoImage(res1)
undo_button = Button(up_frame, text="Undo", image=undo_img, width=35, height=35, font="Times 15 bold", padx=5,
                     bg=background_color, command=lambda: undo_move())
image2 = Image.open('reset.jpg')
res2 = image2.resize((25, 25))
reset_img = ImageTk.PhotoImage(res2)
reset_button = Button(up_frame, text="Reset", image=reset_img, width=35, height=35, font="Times 15 bold", padx=5,
                      bg=background_color, command=lambda: reset_move())
title.grid(row=0, column=0, padx=30, pady=(5, 0))
result.grid(row=1, column=0)
score_name.grid(row=0, column=0)
score_val.grid(row=1, column=0)
high_score_name.grid(row=0, column=0)
high_score_val.grid(row=1, column=0)
undo_button.grid(row=1, column=1, padx=(140, 30))
reset_button.grid(row=1, column=2)


def draw_board(mat):
    for item in frame2.winfo_children():
        item.destroy()
    for x in range(4):
        for y in range(4):
            val = math.log2(mat[x][y])
            if val > 12:
                val = 12
            square = Frame(frame2, bg=colors[int(val)][0], width=140, height=140)
            square.grid(row=x, column=y, padx=5, pady=5)
            if mat[x][y] == 1:
                label = Label(frame2, text="", bg=colors[int(val)][0], fg=colors[int(val)][1], font="Times 40 bold")
            else:
                label = Label(frame2, text=str(mat[x][y]), bg=colors[int(val)][0], fg=colors[int(val)][1],
                              font="Times 40 bold")
            label.grid(row=x, column=y)
    score_val.config(text=str(score))
    high_score_val.config(text=str(high_score))


def init():
    return [[1 for _ in range(4)] for _ in range(4)]


def initialize_first(mat):
    poz = [(k, j) for k in range(4) for j in range(4)]
    p1 = random.randint(0, 15)
    p2 = random.randint(0, 15)
    while p2 == p1:
        p2 = random.randint(0, 15)
    mat[poz[p1][0]][poz[p1][1]] = 2
    mat[poz[p2][0]][poz[p2][1]] = 2


def generate_2_or_4(mat):
    poz = [(x, y) for x in range(4) for y in range(4) if mat[x][y] == 1]
    nr = random.randint(0, len(poz) - 1)
    chance = random.randint(1, 10)
    if chance == 10:
        mat[poz[nr][0]][poz[nr][1]] = 4
    else:
        mat[poz[nr][0]][poz[nr][1]] = 2


def undo_move():
    global can_undo
    global game_lost
    global game_won
    global board
    global score
    if can_undo:
        can_undo = False
        board = [[undo_board[x][y] for y in range(4)] for x in range(4)]
        score = undo_score
        if game_lost:
            game_lost = False
        draw_board(board)
        result.config(text="")


def reset_move():
    global board
    global undo_board
    global score
    global undo_score
    global can_undo
    global game_lost
    global game_won
    global made_first_move
    board = init()
    initialize_first(board)
    undo_board = [[board[x][y] for y in range(4)] for x in range(4)]
    score = 0
    undo_score = 0
    can_undo = False
    made_first_move = False
    game_lost = False
    game_won = False
    result.config(text="")
    draw_board(board)


def winning_condition(mat):
    global game_won
    if not game_won:
        temp = [mat[x][y] for x in range(4) for y in range(4) if mat[x][y] == 2048]
        if len(temp) > 0:
            game_won = True
            result.config(text="You Win", fg="green")
    else:
        result.config(text="")


def losing_condition(mat):
    global game_lost
    empty = [mat[x][y] for x in range(4) for y in range(4) if mat[x][y] == 1]
    if len(empty) == 0:
        rows = [mat[x][y] for x in range(4) for y in range(3) if mat[x][y] == mat[x][y + 1]]
        cols = [mat[x][y] for x in range(4) for y in range(3) if mat[y][x] == mat[y + 1][x]]
        if len(rows) == 0 and len(cols) == 0:
            print('Game over')
            game_lost = True
            result.config(text="Game over", fg="red")


def making_move(mat, mode):
    global can_undo
    global made_first_move
    global undo_board
    global score
    global high_score
    global undo_score
    if not game_lost:
        temp = [[mat[x][y] for y in range(4)] for x in range(4)]
        t_score = 0
        if mode == 1:
            move_up(mat)
            t_score = combine_up(mat)
            move_up(mat)
        elif mode == 2:
            move_right(mat)
            t_score = combine_right(mat)
            move_right(mat)
        elif mode == 3:
            move_down(mat)
            t_score = combine_down(mat)
            move_down(mat)
        elif mode == 4:
            move_left(mat)
            t_score = combine_left(mat)
            move_left(mat)
        are_diff = False
        for x in range(4):
            for y in range(4):
                if mat[x][y] != temp[x][y]:
                    are_diff = True
        if are_diff:
            generate_2_or_4(mat)
            undo_score = score
            score += t_score
            if score > high_score:
                high_score = score
            if made_first_move:
                undo_board = [[temp[x][y] for y in range(4)] for x in range(4)]
            else:
                made_first_move = True
            can_undo = True
        draw_board(mat)
        winning_condition(mat)
        losing_condition(mat)


def move_up(mat):
    for x in range(4):
        y = 0
        while y < 3:
            if mat[y][x] == 1:
                test = [mat[k][x] for k in range(y + 1, 4) if mat[k][x] == 1]
                if len(test) != 4 - (y + 1):
                    for z in range(y + 1, 4):
                        mat[z - 1][x] = mat[z][x]
                        mat[z][x] = 1
                    y -= 1
            y += 1


def combine_up(mat):
    sc = 0
    for x in range(4):
        for y in range(3):
            if mat[y][x] == mat[y + 1][x] and mat[y][x] != 1:
                sc += 2 * mat[y][x]
                mat[y][x] = 2 * mat[y][x]
                mat[y + 1][x] = 1
    return sc


def move_right(mat):
    for x in range(4):
        y = 3
        while y > 0:
            if mat[x][y] == 1:
                test = [mat[x][k] for k in range(y - 1, -1, -1) if mat[x][k] == 1]
                if len(test) != y:
                    for z in range(y - 1, -1, -1):
                        mat[x][z + 1] = mat[x][z]
                        mat[x][z] = 1
                    y += 1
            y -= 1


def combine_right(mat):
    sc = 0
    for x in range(4):
        for y in range(3, 0, -1):
            if mat[x][y] == mat[x][y - 1] and mat[x][y] != 1:
                sc += 2 * mat[x][y]
                mat[x][y] = 2 * mat[x][y]
                mat[x][y - 1] = 1
    return sc


def move_down(mat):
    for x in range(4):
        y = 3
        while y > 0:
            if mat[y][x] == 1:
                test = [mat[k][x] for k in range(y - 1, -1, -1) if mat[k][x] == 1]
                if len(test) != y:
                    for z in range(y - 1, -1, -1):
                        mat[z + 1][x] = mat[z][x]
                        mat[z][x] = 1
                    y += 1
            y -= 1


def combine_down(mat):
    sc = 0
    for x in range(4):
        for y in range(3, 0, -1):
            if mat[y][x] == mat[y - 1][x] and mat[y][x] != 1:
                sc += 2 * mat[y][x]
                mat[y][x] = 2 * mat[y][x]
                mat[y - 1][x] = 1
    return sc


def move_left(mat):
    for x in range(4):
        y = 0
        while y < 3:
            if mat[x][y] == 1:
                test = [mat[x][k] for k in range(y + 1, 4) if mat[x][k] == 1]
                if len(test) != 4 - (y + 1):
                    for z in range(y + 1, 4):
                        mat[x][z - 1] = mat[x][z]
                        mat[x][z] = 1
                    y -= 1
            y += 1


def combine_left(mat):
    sc = 0
    for x in range(4):
        for y in range(3):
            if mat[x][y] == mat[x][y + 1] and mat[x][y] != 1:
                sc += 2 * mat[x][y]
                mat[x][y] = 2 * mat[x][y]
                mat[x][y + 1] = 1
    return sc


def load_data():
    global board
    global undo_board
    global score
    global undo_score
    global high_score
    global can_undo
    global made_first_move
    global game_won
    global game_lost
    with open('data.json', 'r') as file:
        data = json.load(file)
    board = data['board']
    undo_board = data['undo_board']
    score = data['score']
    undo_score = data['undo_score']
    high_score = data['high_score']
    can_undo = data['can_undo']
    made_first_move = data['made_first_move']
    game_won = data['game_won']
    game_lost = data['game_lost']


def save_data():
    if os.stat('data.json').st_size == 0:
        print(board)
        data = {'board': board, 'undo_board': undo_board, 'score': score, 'undo_score': undo_score,
                'high_score': high_score, 'can_undo': can_undo, 'made_first_move': made_first_move,
                'game_won': game_won,
                'game_lost': game_lost}
        with open('data.json', 'w') as file:
            json.dump(data, file)
    else:
        with open('data.json', 'r') as file:
            data = json.load(file)
        data['board'] = board
        data['undo_board'] = undo_board
        data['score'] = score
        data['undo_score'] = undo_score
        if high_score > data['high_score']:
            data['high_score'] = high_score
        data['can_undo'] = can_undo
        data['made_first_move'] = made_first_move
        data['game_won'] = game_won
        data['game_lost'] = game_lost
        with open('data.json', 'w') as file:
            json.dump(data, file)
    game.destroy()


if __name__ == '__main__':
    board = init()
    initialize_first(board)
    undo_board = [[board[x][y] for y in range(4)] for x in range(4)]
    score = 0
    high_score = 0
    undo_score = 0
    can_undo = False
    made_first_move = False
    game_lost = False
    game_won = False
    if os.stat('data.json').st_size != 0:
        load_data()
    draw_board(board)
    game.bind('<Up>', lambda ev: making_move(board, 1))
    game.bind('<Right>', lambda ev: making_move(board, 2))
    game.bind('<Down>', lambda ev: making_move(board, 3))
    game.bind('<Left>', lambda ev: making_move(board, 4))
game.protocol("WM_DELETE_WINDOW", save_data)
game.mainloop()
