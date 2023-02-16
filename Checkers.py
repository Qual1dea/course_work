from tkinter import *
import random
import time
import copy
from tkinter import messagebox

main_win = Tk()
main_win.title('Итальянские Шашки')
board = Canvas(main_win, width=800, height=800, bg='#FFFFFF')
board.pack()

n2_list = ()
ur = 1
k_rez = 0
o_rez = 0
pos_1x = -1
f_hi = True

def image_pawn():
    global pawns
    i1 = PhotoImage(file="figures\\white.png")
    i2 = PhotoImage(file="figures\\white_king.png")
    i3 = PhotoImage(file="figures\\black.png")
    i4 = PhotoImage(file="figures\\black_king.png")
    pawns = [0, i1, i2, i3, i4]

def start_game():
    global game_field
    game_field = [[0, 3, 0, 3, 0, 3, 0, 3],
                  [3, 0, 3, 0, 3, 0, 3, 0],
                  [0, 3, 0, 3, 0, 3, 0, 3],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 0, 1, 0, 1, 0, 1, 0],
                  [0, 1, 0, 1, 0, 1, 0, 1],
                  [1, 0, 1, 0, 1, 0, 1, 0]]

def p_field(x_poz_1, y_poz_1, x_poz_2, y_poz_2):
    global game_field, pawns, red_stroke, green_stroke
    x = 0
    k = 100
    board.delete('all')
    red_stroke = board.create_rectangle(-8, -8, -8, -8, outline="red", width=8)
    green_stroke = board.create_rectangle(-8, -8, -8, -8, outline="green", width=8)
    while x < 8 * k:
        y = 1 * k
        while y < 8 * k:
            board.create_rectangle(x, y, x + k, y + k, fill="black")
            y += 2 * k
        x += 2 * k
    x = 1 * k
    while x < 8 * k:
        y = 0
        while y < 8 * k:
            board.create_rectangle(x, y, x + k, y + k, fill="black")
            y += 2 * k
        x += 2 * k
    for y in range(8):
        for x in range(8):
            z = game_field[y][x]
            if z:
                if (x_poz_1, y_poz_1) != (x, y):
                    board.create_image(x * k, y * k, anchor=NW, image=pawns[z])
    z = game_field[y_poz_1][x_poz_1]
    if z:
        board.create_image(x_poz_1 * k, y_poz_1 * k, anchor=NW, image=pawns[z], tag='ani')
    kx = 1 if x_poz_1 < x_poz_2 else -1
    ky = 1 if y_poz_1 < y_poz_2 else -1
    for i in range(abs(x_poz_1 - x_poz_2)):
        for ii in range(33):
            board.move('ani', 0.03 * k * kx, 0.03 * k * ky)
            board.update()
            time.sleep(0.01)

def position_1(event):
    x, y = (event.x) // 100, (event.y) // 100
    board.coords(green_stroke, x * 100, y * 100, x * 100 + 100, y * 100 + 100)

def position_2(event):
    global pos_1x, pos_1y, pos_2x, pos_2y
    global f_hi
    x, y = (event.x) // 100, (event.y) // 100
    if game_field[y][x] == 1 or game_field[y][x] == 2:
        board.coords(red_stroke, x * 100, y * 100, x * 100 + 100, y * 100 + 100)
        pos_1x, pos_1y = x, y
    else:
        if pos_1x != -1:
            pos_2x, pos_2y = x, y
            if f_hi:
                player_move()
                if not (f_hi):
                    time.sleep(0.5)
                    comp_player()
            pos_1x = -1
            board.coords(red_stroke, -5, -5, -5, -5)

def comp_player():
    global f_hi
    global n2_list
    str_check(1, (), [])
    if n2_list:
        sc = len(n2_list)
        th = random.randint(0, sc - 1)
        dh = len(n2_list[th])
        for i in range(dh - 1):
            list_s = move(1, n2_list[th][i][0], n2_list[th][i][1], n2_list[th][1 + i][0], n2_list[th][1 + i][1])
        n2_list = []
        f_hi = True

    s_k, s_i = skan()
    if not (s_i):
        g_results(2)
    elif not (s_k):
        g_results(1)
    elif f_hi and not (list_hi()):
        g_results(3)
    elif not (f_hi) and not (list_sc()):
        g_results(3)

def g_results(s):
    global f_hi
    z = 'Игра завершена'
    if s == 1:
        i = messagebox.askyesno(title=z, message='Вы победили!\nНажмите "Да" что бы начать заново.', icon='info')
    if s == 2:
        i = messagebox.askyesno(title=z, message='Вы проиграли!\nНажмите "Да" что бы начать заново.', icon='info')
    if s == 3:
        i = messagebox.askyesno(title=z, message='Ходов больше нет.\nНажмите "Да" что бы начать заново.', icon='info')
    if i:
        start_game()
        p_field(-1, -1, -1, -1)
        f_hi = True


def list_hi():
    list_s = check_move_i1([])
    if not (list_s):
        list_s = check_move_i2([])
    return list_s

def examin_hi(tur, list_s):
    global game_field, k_rez, o_rez
    global ur
    if not (list_s):
        list_s = list_hi()
    if list_s:
        k_pole = copy.deepcopy(game_field)
        for ((poz1_x, poz1_y), (poz2_x, poz2_y)) in list_s:
            t_spisok = move(0, poz1_x, poz1_y, poz2_x, poz2_y)
            if t_spisok:
                examin_hi(tur, t_spisok)
            else:
                if tur < ur:
                    str_check(tur + 1, (), [])
                else:
                    s_k, s_i = skan()
                    o_rez += (s_k - s_i)
                    k_rez += 1
            game_field = copy.deepcopy(k_pole)
    else:
        s_k, s_i = skan()
        o_rez += (s_k - s_i)
        k_rez += 1


def list_sc():
    list_s = check_move_k1([])
    if not (list_s):
        list_s = check_move_k2([])
    return list_s

def str_check(tur, n_spisok, list_s):
    global game_field
    global n2_list
    global l_rez, k_rez, o_rez
    if not (list_s):
        list_s = list_sc()
    if list_s:
        k_pole = copy.deepcopy(game_field)
        for ((poz1_x, poz1_y), (poz2_x, poz2_y)) in list_s:
            t_spisok = move(0, poz1_x, poz1_y, poz2_x, poz2_y)
            if t_spisok:
                str_check(tur, (n_spisok + ((poz1_x, poz1_y),)), t_spisok)
            else:
                examin_hi(tur, [])
                if tur == 1:
                    t_rez = o_rez / k_rez
                    if not (n2_list):
                        n2_list = (n_spisok + ((poz1_x, poz1_y), (poz2_x, poz2_y)),)
                        l_rez = t_rez
                    else:
                        if t_rez == l_rez:
                            n2_list = n2_list + (n_spisok + ((poz1_x, poz1_y), (poz2_x, poz2_y)),)
                        if t_rez > l_rez:
                            n2_list = ()
                            n2_list = (n_spisok + ((poz1_x, poz1_y), (poz2_x, poz2_y)),)
                            l_rez = t_rez
                    o_rez = 0
                    k_rez = 0
            game_field = copy.deepcopy(k_pole)
    else:
        s_k, s_i = skan()
        o_rez += (s_k - s_i)
        k_rez += 1


def skan():
    global game_field
    s_i = 0
    s_k = 0
    for i in range(8):
        for ii in game_field[i]:
            if ii == 1: s_i += 1
            if ii == 2: s_i += 3
            if ii == 3: s_k += 1
            if ii == 4: s_k += 3
    return s_k, s_i


def player_move():
    global pos_1x, pos_1y, pos_2x, pos_2y
    global f_hi
    f_hi = False
    list_s = list_hi()
    if list_s:
        if ((pos_1x, pos_1y), (pos_2x, pos_2y)) in list_s:
            t_spisok = move(1, pos_1x, pos_1y, pos_2x, pos_2y)
            if t_spisok:
                f_hi = True
        else:
            f_hi = True
    board.update()


def move(f, poz1_x, poz1_y, poz2_x, poz2_y):
    global game_field
    if f: p_field(poz1_x, poz1_y, poz2_x, poz2_y)
    if poz2_y == 0 and game_field[poz1_y][poz1_x] == 1:
        game_field[poz1_y][poz1_x] = 2
    if poz2_y == 7 and game_field[poz1_y][poz1_x] == 3:
        game_field[poz1_y][poz1_x] = 4
    game_field[poz2_y][poz2_x] = game_field[poz1_y][poz1_x]
    game_field[poz1_y][poz1_x] = 0

    kx = ky = 1
    if poz1_x < poz2_x: kx = -1
    if poz1_y < poz2_y: ky = -1
    x_poz, y_poz = poz2_x, poz2_y
    while (poz1_x != x_poz) or (poz1_y != y_poz):
        x_poz += kx
        y_poz += ky
        if game_field[y_poz][x_poz] != 0:
            game_field[y_poz][x_poz] = 0
            if f: p_field(-1, -1, -1, -1)
            if game_field[poz2_y][poz2_x] == 3 or game_field[poz2_y][poz2_x] == 4:
                return check_move_k1p([], poz2_x, poz2_y)
            elif game_field[poz2_y][poz2_x] == 1 or game_field[poz2_y][poz2_x] == 2:
                return check_move_i1p([], poz2_x, poz2_y)
    if f: p_field(poz1_x, poz1_y, poz2_x, poz2_y)

def check_move_k1(list_s):
    for y in range(8):
        for x in range(8):
            list_s = check_move_k1p(list_s, x, y)
    return list_s


def check_move_k1p(list_s, x, y):
    if game_field[y][x] == 3:
        for ix, iy in (-1, 0), (-1, 1), (1, 0), (1, 1):
            if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                if game_field[y + iy][x + ix] == 1 or game_field[y + iy][x + ix] == 2:
                    if game_field[y + iy + iy][x + ix + ix] == 0:
                        list_s.append(((x, y), (x + ix + ix, y + iy + iy)))
    if game_field[y][x] == 4:
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            osh = 0
            for i in range(1, 8):
                if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                    if osh == 1:
                        list_s.append(((x, y), (x + ix * i, y + iy * i)))
                    if game_field[y + iy * i][x + ix * i] == 1 or game_field[y + iy * i][x + ix * i] == 2:
                        osh += 1
                    if game_field[y + iy * i][x + ix * i] == 3 or game_field[y + iy * i][x + ix * i] == 4 or osh == 2:
                        if osh > 0: list_s.pop()
                        break
    return list_s


def check_move_k2(spisok):
    for y in range(8):
        for x in range(8):
            if game_field[y][x] == 3:
                for ix, iy in (-1, 1), (1, 1):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        if game_field[y + iy][x + ix] == 0:
                            spisok.append(((x, y), (x + ix, y + iy)))
                        if game_field[y + iy][x + ix] == 1 or game_field[y + iy][x + ix] == 2:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if game_field[y + iy * 2][x + ix * 2] == 0:
                                    spisok.append(((x, y), (x + ix * 2, y + iy * 2)))
            if game_field[y][x] == 4:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0
                    for i in range(1, 8):
                        if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                            if game_field[y + iy * i][x + ix * i] == 0:
                                spisok.append(((x, y), (x + ix * i, y + iy * i)))
                            if game_field[y + iy * i][x + ix * i] == 1 or game_field[y + iy * i][x + ix * i] == 2:
                                osh += 1
                            if game_field[y + iy * i][x + ix * i] == 3 or game_field[y + iy * i][
                                x + ix * i] == 4 or osh == 2:
                                break
    return spisok

def check_move_i1(list_s):
    list_s = []
    for y in range(8):
        for x in range(8):
            list_s = check_move_i1p(list_s, x, y)
    return list_s

def check_move_i1p(list_s, x, y):
    if game_field[y][x] == 1:
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                if game_field[y + iy][x + ix] == 3 or game_field[y + iy][x + ix] == 4:
                    if game_field[y + iy + iy][x + ix + ix] == 0:
                        list_s.append(((x, y), (x + ix + ix, y + iy + iy)))
    if game_field[y][x] == 2:
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            osh = 0
            for i in range(1, 8):
                if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                    if osh == 1:
                        list_s.append(((x, y), (x + ix * i, y + iy * i)))
                    if game_field[y + iy * i][x + ix * i] == 3 or game_field[y + iy * i][x + ix * i] == 4:
                        osh += 1
                    if game_field[y + iy * i][x + ix * i] == 1 or game_field[y + iy * i][x + ix * i] == 2 or osh == 2:
                        if osh > 0: list_s.pop()
                        break
    return list_s

def check_move_i2(list_s):
    for y in range(8):
        for x in range(8):
            if game_field[y][x] == 1:
                for ix, iy in (-1, -1), (1, -1):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        if game_field[y + iy][x + ix] == 0:
                            list_s.append(((x, y), (x + ix, y + iy)))
                        if game_field[y + iy][x + ix] == 3 or game_field[y + iy][x + ix] == 4:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if game_field[y + iy * 2][x + ix * 2] == 0:
                                    list_s.append(((x, y), (x + ix * 2, y + iy * 2)))
            if game_field[y][x] == 2:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    oph = 0
                    for i in range(1, 8):
                        if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                            if game_field[y + iy * i][x + ix * i] == 0:
                                list_s.append(((x, y), (x + ix * i, y + iy * i)))
                            if game_field[y + iy * i][x + ix * i] == 3 or game_field[y + iy * i][x + ix * i] == 4:
                                oph += 1
                            if game_field[y + iy * i][x + ix * i] == 1 or game_field[y + iy * i][
                                x + ix * i] == 2 or oph == 2:
                                break
    return list_s

def run():
    image_pawn()
    start_game()
    p_field(-1, -1, -1, -1)
    board.bind("<Motion>", position_1)
    board.bind("<Button-1>", position_2)
    mainloop()