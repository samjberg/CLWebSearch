from rich import console, table
from rich.repr import Result
from rich.table import Table
from rich.segment import Segment
from rich.console import Console, ConsoleOptions, RenderableType
from rich.text import Text
from rich.style import Style
from rich.color import ANSI_COLOR_NAMES as COLOR_DICT
from rich import print, inspect
from typing import Union
from os import get_terminal_size
from logger import log
import json
from scrollable import Scrollable
from parsehtml import parse_raw_html
from linesrenderable import LinesRenderable




class SelectableTable(LinesRenderable):
    def __init__(self, rows: list[list[Text]] | list[Text], highlight_color='yellow'):
        super(SelectableTable, self).__init__(rows, True, 1)
        #currently selected index
        self.curr_idx = 0
        self.prev_idx = 0
        self.highlight_color = highlight_color

    
    def move_selection(self, n: int):
        new_idx = min(max(self.curr_idx + n, 0), len(self)-1)
        if new_idx != self.curr_idx:
            self.set_row_color(self.curr_idx, '')
        self.set_row_color(new_idx, self.highlight_color)
        self.prev_idx = self.curr_idx
        self.curr_idx = new_idx
        log(f'grid[{self.curr_idx}][1]: {self.grid[self.curr_idx][1]}')


    def move_selection_down(self, n: int):
        self.move_selection(n)

    def move_selection_up(self, n: int):
        self.move_selection(-n)


