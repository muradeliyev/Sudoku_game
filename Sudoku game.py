from tkinter import *
import functions as funcs
import time
import _thread

# THEME
line_color = 'gray'
text_color = 'blue'
background_color = 'white'

g = 9 # grid variable
active = (None, None)
board = [[0 for i in range(9)] for _ in range(9)]

pen = Tk()
pen.title("Sudoku")

####### MENU #########
menu = Menu(pen)
menu.add_command(label='Solve', command=lambda: _thread.start_new_thread(funcs.solve, (board,)))
menu.add_command(label='Create game', command=funcs.create_new)

pen.config(menu=menu)

canvas = Canvas(pen, width=400, height=400, bg=background_color)
canvas.pack()

funcs.draw_lines()

pen.minsize(400, 400)
pen.resizable(False, False)
pen.mainloop()
