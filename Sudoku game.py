from tkinter import *
import time
import _thread

# THEME
line_color = 'gray'
text_color = 'blue'
background_color = 'white'

g = 9 # grid variable
active = (None, None)
board = [[0 for i in range(9)] for _ in range(9)]
#####################################################################################################
def solve(board):
    draw_game(board)

    find = find_empty()
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if is_valid(i, row, col):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False

def mouse_handler(event):
    global active
    row, col = get_grid(event)
    w = float(canvas['height']) / g

    if (row, col) != active:
        canvas.delete('active')
        x = col * w
        y = row * w
        canvas.create_rectangle(x, y, x+w, y+w, outline='green', fill='', tags='active', width=5)
        active = (row, col)

    else:
        active = (None, None)
        canvas.delete('active')

def key_handler(event):
    try:
        char = int(event.char)
        if is_valid(char, *active):
            s = float(canvas['width']) / g
            row, col = active
            if board[row][col] != 0: canvas.delete('last')
            canvas.dtag('number', 'last')
            canvas.create_text(col*s+s/2, row*s+s/2, text=char, font=('Arial', 20), fill=text_color, tags=('number', 'last'))
            board[row][col] = char

    except: pass

def move(x, y):
    global active
    row, col = active
    w = float(canvas['height']) / g

    col += x
    row += y

    if col == 9: col = 0
    elif col == -1: col = 8

    if row == 9: row = 0
    elif row == -1: row = 8

    canvas.delete('active')
    x = col * w
    y = row * w
    canvas.create_rectangle(x, y, x + w, y + w, outline='green', fill='', tags='active', width=5)
    active = (row, col)

def print_board(event):
    for i in range(9):
        for j in range(9):
            print(f"{board[i][j]}", end=(' | ' if (j!=8 and (j+1)%3==0) else ' '))
        print('\n---------------------' if i!=8 and (i+1)%3==0 else '')
    print("\n\n")

def create_new():
    global board
    board = [[0 for i in range(9)] for _ in range(9)]
    canvas.delete('number')
    canvas.bind("<Button-1>", mouse_handler)
    pen.bind("<Key>", key_handler)
    pen.bind("<Left>", lambda e: move(-1, 0))
    pen.bind("<Right>", lambda e: move(1, 0))
    pen.bind("<Up>", lambda e: move(0, -1))
    pen.bind("<Down>", lambda e: move(0, 1))

    pen.bind("<space>", print_board)

def find_empty():
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j

def draw_game(board):
    canvas.delete('number')
    for i in range(9):
        for j in range(9):
            write_number(board[i][j], i, j)
    # time.sleep(0.1)
        
def draw_lines():
    # horizontal lines
    for i in range(1, g):
        canvas.create_line(0, i*float(canvas['height'])/g,
                           float(canvas['width']), i*float(canvas['height'])/g,
                           fill=line_color, width=(1 if i%3!=0 else 3))
    # vertical lines
    for i in range(1, g):
        canvas.create_line(i*float(canvas['width'])/g, 0,
                           i*float(canvas['width'])/g, float(canvas['height']),
                           fill=line_color, width=(1 if i%3!=0 else 3))

def write_number(n, row, col):
    s = float(canvas['width'])/g
    if board[row][col] != 0:
        canvas.create_text(col*s+s/2, row*s+s/2, text=str(n), font=('Arial', 20), fill=text_color, tags='number')

def new_stage(n, row, col):
    b = board.copy()
    b[row][col] = n
    return b

def get_grid(event):
    col = int(event.x / (float(canvas['width']) / g))
    row = int(event.y / (float(canvas['height']) / g))
        
    return row, col

def check_in_horizontal(n, row, col):
    # from left to right
    for i in range(len(board[row])):
        if i == col: continue
        if board[row][i] == n:
            return True
    return False

def check_in_vertical(n, row, col):
    # from top to bottom
    for i in range(len(board)):
        if i == row: continue
        if board[i][col] == n:
            return True
    return False

def check_in_box(n, row, col):
    # in 3x3 boxes
    r = row // 3 * 3
    c = col // 3 * 3
    for i in range(3):
        for j in range(3):
            if r+i == row and c+j == col: continue
            if board[r+i][c+j] == n:
                return True
    return False

def check_knight_move(n, row, col):
    moves = [
        [-1, -2],
        [1, -2],
        [2, -1],
        [2, 1],
        [1, 2],
        [-1, 2],
        [-2, 1],
        [-2, -1]
    ]
    for x, y in moves:
        r = row + y
        c = col + x
        if 0 <= c <= 8 and 0 <= r <= 8:
            if board[r][c] == n:
                return True
    return False

def is_valid(n, row, col):
    return not check_in_vertical(n, row, col) and not check_in_horizontal(n, row, col) and not check_in_box(n, row, col) and not check_knight_move(n, row, col)
#####################################################################################################
pen = Tk()
pen.title("Sudoku")

####### MENU #########
menu = Menu(pen)
menu.add_command(label='Solve', command=lambda: _thread.start_new_thread(solve, (board,)))
menu.add_command(label='Create game', command=create_new)

pen.config(menu=menu)

canvas = Canvas(pen, width=400, height=400, bg=background_color)
canvas.pack()

draw_lines()

pen.minsize(400, 400)
pen.resizable(False, False)
pen.mainloop()