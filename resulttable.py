from rich.repr import Result
from rich.table import Table
from rich.segment import Segment
from rich.console import Console, ConsoleOptions, RenderableType
from rich.text import Text
from rich.style import Style
from rich.color import ANSI_COLOR_NAMES as COLOR_DICT
from typing import Union
from entry import Entry
from os import get_terminal_size
from logger import log
from renderedpage import RenderedPage



def remove_color_tags(s: str):
    if isinstance(s, Entry):
        entry = s
        s = entry.text
        if not s:
            return entry
        while s.startswith('['):
            log(f'in remove_color_tags while loop.  s:{s}')
            end_idx = s.find(']')
            if end_idx == -1:
                return s
            s = s[end_idx+1:]
        return s
    else:
        log(f'in remove_color_tags, s:{s}')
        if not s:
            log(f'in "if not s" block in remove_color_tags.  s:{s}')
            return s
        while s.startswith('['):
            log(f'in remove_color_tags while loop.  s:{s}')
            end_idx = s.find(']')
            if end_idx == -1:
                return s
            s = s[end_idx+1:]
        return s




def get_colors_in_style(style: str):
    words = style.split(' ')
    colors = []
    for word in words:
        if word in COLOR_NAMES:
            colors.append(word)
    return colors

class Pos:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Pos):
            return Pos(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple):
            if len(other) == 2:
                return Pos(self.x + other[0], self.y + other[1])
            else:
                raise ValueError(f'Error, tuples can be added to Pos\'s, but must be length 2.  Got length: {len(other)}')
        else:
            raise TypeError(f'Error, can only add Pos or length 2 tuple to Pos.  Got: {type(other)}')


    def __sub__(self, other):
        if isinstance(other, Pos):
            return Pos(self.x - other.x, self.y - other.y)
        elif isinstance(other, tuple):
            if len(other) == 2:
                return Pos(self.x - other[0], self.y - other[1])
            else:
                raise ValueError(f'Error, tuples can be added to Pos\'s, but must be length 2.  Got length: {len(other)}')
        else:
            raise TypeError(f'Error, can only add Pos or length 2 tuple to Pos.  Got: {type(other)}')



    def __getitem__(self, idx: int):
        if idx == 0 or idx == 'x':
            return self.x
        elif idx == 1 or idx == 'y':
            return self.y
        raise IndexError('Error, index out of bounds')

    def __setitem__(self, idx: int, val: int):
        if idx == 0 or idx == 'x':
            self.x = val
        elif idx == 1 or idx == 'y':
            self.y = val
        raise IndexError('Error, index out of bounds')

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __rich_console__(self, console: Console, options: ConsoleOptions):
        return f'({self.x}, {self.y})'


COLOR_NAMES = list(COLOR_DICT.keys())




class ResultTable:
    def __init__(self, column_names:list[str], title:str='', rows:list[list[Segment]]|None=[]):
        self.column_names:list[str] = column_names
        self.grid:list[list[Text]] = []
        self.original_styles:list[list[str]] = []
        self.segments = []
        self.title = title
        self.highlighted_row = 0

        # self.columns = self.table.columns
        if rows:
            for row in rows:
                grid_row = []
                for seg in row:
                    if isinstance(seg, Segment):
                        s = seg.text
                        style = seg.style if seg.style else ''
                        text_seg = Text(seg.text, style)
                        grid_row.append(text_seg)
                    elif isinstance(seg, Text):
                        grid_row.append(seg)
                    elif isinstance(seg, str):
                        grid_row.append(Text(seg))
                    else:
                        raise TypeError(f'Error, each individual element of rows must be Text|str|Segment, got: {type(seg)}')
                # grid_row.append(Segment.line())
                self.grid.append(grid_row)

        for row in self.grid:
            self.original_styles.append([str(text.style) for text in row])


                # if all([isinstance(x, Segment) for x in row]):
                #     self.grid.append(row)
                # else:
                #     row = [seg if isinstance(seg, Segment) else Segment(seg) for seg in row]
                #     self.grid.append(row)

    def get_color_at(self, x: int, y: int) -> list[str]:
        text = self.grid[y][x]
        style = str(text.style)
        return get_colors_in_style(style)


    def set_color_at(self, x: int, y: int, color: str) -> None:
        self.grid[y][x] = Text(str(self.grid[y][x]), color)
        # self.grid[y][x].style = color



    def get_row(self, row_index: int):
        return self.grid[row_index]


    def update_entry(self, row: int, col:str|int, val: str, color:str=''):
        col_index = self.column_names.index(col) if isinstance(col, str) else col
        if not color:
            color = self.get_color_at(col_index, row)[0]
        self.grid[row][col_index] = Text(val, color)

    def set_row_color(self, row_idx: int, color: str):
        for x in range(len(self.grid[row_idx])):
            self.set_color_at(x, row_idx, color)

    def highlight_row(self, row_idx, color='yellow'):
        log(f'Highlighting row: {row_idx}')
        for y, row in enumerate(self.grid):
            if y == row_idx:
                continue
            # if all([self.get_color_at(x, idx) == color for x, entry in enumerate(row)]):
            for x, text in enumerate(row):
                self.set_color_at(x, y, self.original_styles[y][x])

            # self.set_row_color(y, 'gray')
        self.set_row_color(row_idx, color)
        self.highlighted_row = row_idx


    def get_table(self, start=0, up_to=-1):
        if up_to == -1:
            up_to = len(self.grid)
        table = Table()
        for name in self.column_names:
            table.add_column(name)
        for i in range(start, up_to):#self.grid:
            row = self.grid[i]
            table.add_row(*row)
        return table



    def get_height(self, console: Console, start=0, up_to=-1):
        table = self.get_table(start, up_to)
        lines = console.render_lines(table)
        header_height = 3
        return max(len(lines) - header_height, 1)

    def get_row_height(self, console: Console, row_idx: int):
        return max(self.get_height(console, row_idx, row_idx+1), 1)


    # def get_table(self):
    #     table = Table(
    #     pass



    def __len__(self):
        return len(self.grid)

    def __iter__(self):
        for row in self.grid:
            yield row

    def __getitem__(self, idx):
        if isinstance(idx, int):
            return self.grid[idx]

        if isinstance(idx, slice):
            start = idx.start
            stop = idx.stop if idx.stop else len(self.grid)
            step = idx.step if idx.step else 1
            res = []
            for i in range(start, stop, step):
                res.append(self.grid[i])
            return res

        raise IndexError(f'Error, invalid index into ResultTable')





    def __rich_console__(self, console: Console, options: ConsoleOptions):
        table = self.get_table()
        yield table
        # lines = console.render_lines(table)
        # r = table.rows[0]
        # for line in lines:
        #     for seg in line:
        #         yield seg
        #     yield Segment('\n')


    def __repr__(self):
        s = ''
        for row in self.grid:
            s += '    '.join([str(entry) for entry in row])
        return s
    
    def __str__(self):
        s = ''
        for row in self.grid:
            s += '    '.join([str(entry) for entry in row]) + '\n'
        return s


    # def table(self) -> RenderableType:
    #     return self.__rich_console__()
