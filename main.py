from tkinter import *
import random
from solver import SudokuSolver

class CGL(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.grid(column=0, row=0)
        self.configure(height=600, width=600)
        self.paused = True
        self.solver = SudokuSolver()
        
        self.CELL_SIZE = 50
        self.COLS = 9
        self.ROWS = 9
        self.CANVAS_DIM = (self.CELL_SIZE * self.COLS, self.CELL_SIZE * self.COLS)

        #INITIALIZE CELLS
        self.cells = [[0] * self.COLS for i in range(self.ROWS)]

        self.buildUI()
        self.gen()
            
    def clear_cells(self):
        self.cells = [[0] * self.COLS for i in range(self.ROWS)]
        self.draw_cells(False)

    def buildUI(self):
        # MAKE BUTTON BAR
        button_bar = Frame(self, padx=10, pady=10)
        button_bar.grid(column=0, row=0)
            
        gen = Button(button_bar, text="gen", command=self.gen)
        gen.grid(column=0, row=0)

        clear = Button(button_bar, text="clear", command=self.clear_cells)
        clear.grid(column=1, row=0)

        self.play = Button(button_bar, text="solve", command=self.solve)
        self.play.grid(column=2, row=0)

        # MAKE CANVAS/GRID CONSTRUCT
        self.canvas = Canvas(self, width=self.CANVAS_DIM[0], height=self.CANVAS_DIM[1], bg="white")
        self.canvas.grid(column=0, row=1)
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<KeyPress>", self.key_press)
        
        numbar = Frame(self, width=self.CELL_SIZE, height=self.CANVAS_DIM[1], padx=10)
        numbar.grid(column=1,row=1)
        
        self.num_labels = []
        
        for i in range(1, 10):
            temp_f = Frame(numbar, width=self.CELL_SIZE, height=self.CELL_SIZE)
            label = Label(temp_f, text=str(i), padx=14, pady=10, bg="white", bd=2)
            temp_f.grid(column=0,row=i-1)
            label.pack()
            self.num_labels += [label]
            
        self.select_num(1)
            
        self.draw_grid()
        self.draw_cells(False)

    def key_press(self, ev):
        if ev.char.isnumeric() and int(ev.char) > 0:
            self.select_num(int(ev.char))

    def select_num(self, num):
        self.selected_num = num
        for i, nl in enumerate(self.num_labels):
            nl.config(bg = "red" if i == num-1 else "white") 
        
    def canvas_click(self, event):
        row = event.x // self.CELL_SIZE
        col = event.y // self.CELL_SIZE
        self.cells[col][row] = self.selected_num
        self.draw_cells(False)

    def solve(self):
        sol = self.solver.solve(self.cells)
        if sol:
            self.cells = sol
            self.draw_cells()
        else:
            self.draw_cells(True)
            self.after(100, self.draw_cells)
        
    def gen(self):
        self.clear_cells()
        x_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        y_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        random.shuffle(x_list)
        random.shuffle(y_list)
        random.shuffle(num_list)
        
        coords = zip(x_list, y_list, num_list)

        for c in coords:
            self.cells[c[0]][c[1]] = c[2]
            
        self.draw_cells(False)

    def draw_grid(self, warning=False):
        self.canvas.create_rectangle(0,
                                     0,
                                     self.CANVAS_DIM[0],
                                     self.CANVAS_DIM[1],
                                     fill= "red" if warning else "white")
        
        for i in range(0, self.CANVAS_DIM[0], self.CELL_SIZE):
            lw = 3 if (i / self.CELL_SIZE) % 3 == 0 else 1
            self.canvas.create_line(i, 0, i, self.CANVAS_DIM[1], width=lw)

        for i in range(0, self.CANVAS_DIM[1], self.CELL_SIZE):
            lw = 3 if (i / self.CELL_SIZE) % 3 == 0 else 1
            self.canvas.create_line(0, i, self.CANVAS_DIM[0], i, width=lw)

    def draw_cells(self, warning=False):
        self.draw_grid(warning)
        sc = self.cells
        for i in range(len(sc)):
            y_pos = i * self.CELL_SIZE
            for j in range(len(sc[0])):
                x_pos = j * self.CELL_SIZE
                if sc[i][j] != 0:
                    self.canvas.create_text(x_pos + self.CELL_SIZE // 2,
                                            y_pos + 8 + self.CELL_SIZE // 2, 
                                            text=str(sc[i][j]),
                                            font=("Helvetica", "38"))

root = Tk()
game = CGL(root)
root.mainloop()

