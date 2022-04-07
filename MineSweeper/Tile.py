from enum import Enum
from tkinter.constants import HIDDEN

colors = ['#7c7a77', '#cfd0d2', '#fbd083', '#ed2939']

class TileState(Enum):
    HIDDEN = 0
    FLAGGED = 1
    VISIBLE = 2

class Tile:

    def __init__(self, row, col, width, font, canvas):
        self.canvas = canvas
        self.row = row
        self.col = col
        self.width = width
        self.color = colors[0]
        self.font = font

        self.state = TileState.HIDDEN
        
        self.is_bomb = False
        self.num = 0
        
        self.tile_area = canvas.create_rectangle(self.get_x_pos(0), 
                                                 self.get_y_pos(0),
                                                 self.get_x_pos(1), 
                                                 self.get_y_pos(1), 
                                                 fill=self.color)
        # self.canvas.create_text(self.get_x_pos(0)+width/2, self.get_y_pos(0)+width/4, text=16*row + col)
        # self.risk_text = self.canvas.create_text(self.get_x_pos(0)+width/2, self.get_y_pos(0)+3*width/4, text=1)
        
        text_x = self.width/2 + self.col * self.width
        text_y = self.width/2 + self.row * self.width
        
        self.text_area = canvas.create_text(text_x, text_y, 
                                            font=self.font, text="")

    def get_x_pos(self, col_number):
        return (self.col + col_number)*self.width
    
    def get_y_pos(self, row_number): 
        return (self.row + row_number)*self.width

    def update_tile(self):

        if self.state == TileState.VISIBLE:
            self.set_color(1)
            if self.is_bomb: self.set_color(3)
            elif self.num != 0:
                self.canvas.itemconfig(self.text_area, 
                                       text=str(self.num), 
                                       fill=self.color)
        elif self.state == TileState.FLAGGED:
            self.set_color(2)
        elif self.state == TileState.HIDDEN:
            self.set_color(0)
    
    def update_risk(self, risk):
        self.canvas.itemconfig(self.risk_text, text='{:.2f}'.format(risk))

    def set_color(self, color_number):
        self.canvas.itemconfig(self.tile_area, fill=colors[color_number])

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def get_bomb(self):
        return self.is_bomb
    
    def set_bomb(self):
        self.is_bomb = True

    def force_flag(self):
        self.state = TileState.FLAGGED
        self.update_tile()

    def get_state(self):
        return self.state

    def open_tile(self):

        if self.state == TileState.HIDDEN:
            self.state = TileState.VISIBLE
            self.update_tile()

    def toggle_flag(self):
        if self.state == TileState.HIDDEN:
            self.state = TileState.FLAGGED
            self.update_tile()
            return 1
        elif self.state == TileState.FLAGGED:
            self.state = TileState.HIDDEN
            self.update_tile()
            return -1
        else:
            return 0
            
    def get_tile_number(self):
        return self.num

    def set_tile_number(self, num, color):
        self.num = num
        self.color = color
