import enum
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



# def make_table(column_names:list[str], rows: list[list[RenderableType]], start=0, up_to=-1):
#     if up_to == -1:
#         up_to = len(rows)
#     table = Table()
#     for name in column_names:
#         table.add_column(name)
#     for i in range(start, up_to):#grid:
#         row = rows[i]
#         for j, seg in enumerate(row):
#             if isinstance(seg, Segment):
#                 # log(f'Found segment which would cause problems.  Converting to text with the following.')
#                 # log(f'\ttext: {seg.text}\n\tstyle: {str(seg.style)}\n\n')
#                 row[j] = Text(seg.text, str(seg.style))
#         table.add_row(*row)
#     return table
#
def make_table(column_names:list[str], rows: list[list[RenderableType]], start=0, up_to=-1):
    if up_to == -1:
        up_to = len(rows)
    table = Table()
    for name in column_names:
        table.add_column(name)
    for j in range(start, up_to):#grid:
        curr_row = rows[j]
        new_row = []
        for i, seg in enumerate(curr_row):
            if isinstance(seg, Segment):
                new_entry = Text(seg.text, str(seg.style))
            elif isinstance(seg, Text):
                new_entry = seg
            elif isinstance(seg, str):
                new_entry = Text(seg)
            else:
                raise TypeError(f'Each individual entry must be Segment|Text|str')
            new_row.append(new_entry)
        table.add_row(*new_row)
    return table




def next_whitespace(s: str, start=0):
    for i, c in enumerate(s[start:]):
        if c.isspace():
            return i + start
    return -1

def get_space_indices(s: str):
    first_space_index = next_whitespace(s)
    if first_space_index == -1:
        return []
    space_indices = [first_space_index]
    i = first_space_index
    while i < len(s):
        #find next non_space
        for ii in range(i+1, len(s)):
            if not s[ii].isspace():
                i = ii
                break
        i = next_whitespace(s, i+1)
        if i == -1:
            break
        else:
            space_indices.append(i)
        i += 1
    return space_indices

def count_lines(line: list[Segment], width=270):
    '''Counts the number of actual lines taken up by a line (as a list of Segments)'''
    length = 0
    explicit_newlines = 0
    remainder = 0
    # for seg in line:
    #
    #
    #
    #
    # pass




def line_to_segments(line: str, preserve_whitespace=True) -> list[Segment]:
    '''Convert a line(str) to a list of Segments, preserving whitespace'''
    space_indices = get_space_indices(line)
    segments = []
    prev_idx = 0
    for idx in space_indices:
        segments.append(Segment(line[prev_idx:idx]))
        prev_idx = idx
    segments.append(Segment(line[prev_idx:]))
    if not preserve_whitespace:
        segments = [Segment(seg.text.replace(' ', ''), seg.style) for seg in segments]
    return segments





class LinesRenderable(Scrollable):
    def __init__(self, val: list[list[Text|Segment|str]] | list[Text|Segment|str] |  list[str], as_table=False, scroll_mult=1):
        super().__init__(scroll_mult)
        self.grid:list[list] = []
        self.is_table = as_table
        self.console = Console()
        self.column_names = [str(name) for name in val[0]] if as_table else []
        self._unset_colors = []
        log(f'column_names: [{' ,'.join(self.column_names)}]')
        log(f'column_names types: [{' ,'.join([str(type(name)) for name in self.column_names])}]')
        # if self.is_table:
        #     self.grid = val
        #     # tab.
        # else:
        for line in val:
            row = []
            if isinstance(line, list):
                for seg in line:
                    if isinstance(seg, Segment):
                        if type(seg.style) == Style:
                            row.append(seg)
                        else:
                            row.append(Segment(seg.text, None))
                    elif isinstance(seg, Text) and type(seg) != str:
                        text = str(seg)
                        if not seg.style:
                            style = None
                        else:
                            style = seg.style if isinstance(seg.style, Style) else Style(color=seg.style)
                        new_seg = Segment(text, style)
                        row.append(new_seg)
                        # if isinstance(seg.style, Style) | isinstance(seg.style, str):
                        #     row.append(Segment(str(seg), seg.style))#shut up linter, yes it absolutely literally can
                        # else:
                        #     row.append(Segment(str(seg), None))
                    elif isinstance(seg, str):
                        # log(f'seg is str: {type(line)}, line: {str(line)}')
                        row.append(Segment(seg, None))# if not as_table else row.append(seg)
                    else:
                        raise TypeError(f'Error, each individual component must be Segment|Text|str.  Got: {type(seg)}')
            elif isinstance(line, RenderableType):
                log('ALKJGSDKLJSGDKJLJDGSJGKLAJSGKLGJSDKLDGJSKLSDGJKLGS')
                parts = line_to_segments(str(line))
                for part in parts:
                    row.append(part)
            else:
                raise TypeError(f'Error, each line of val must be list|RenderableType, got: {type(line)}')

            self.grid.append(row)

        self.height = len(self.grid)
        if self.is_table:
            log(f'Before pruning, grid[0] url: {self.grid[0][1]}')
            self.column_names = [str(name) for name in self.column_names]
            self.grid = self.grid[1:]
            self.table = make_table(self.column_names, self.grid)
        else:
            self.table = Table()

    # def get_height2(self, start=0, end=-1):
    #     if end


    def get_height(self, start=0, end=-1):
        if end == -1:
            end = len(self) - 1
        if self.is_table:
            header_height = 3
            log(f'console width: {self.console.width}')
            if start==0 and end==-1:
                return len(self.console.render_lines(make_table(self.column_names, self.grid))) - header_height
            else:
                if start == 0:
                    return len(self.console.render_lines(make_table(self.column_names, self.grid[:end]))) - header_height
                else:
                    return len(self.console.render_lines(make_table(self.column_names, self.grid[start:end]))) - header_height
        else:
            return end - start
            total_length = 0
            explicit_newlines = 0
            remaineder = 0
            for line in self.grid[start:end]:
                for seg in line:
                    s = str(seg)

    def set_color_at(self, x: int, y: int, color:str):
        seg = self.grid[y][x]
        if isinstance(seg, Segment):
            text = seg.text
        elif isinstance(seg, Text):
            text = str(seg)
        else:
            raise TypeError(f'Error, SelectableTable elements must be Segment|Text.  Got: {type(seg)}')


        # style = Style(color=color)
        # log(f'In set_color_at.  Setting color of ({x},{y}) to {str(style)}, type: {type(self.grid[y][x])}')
        self.grid[y][x] = Segment(text, color)

    def set_row_color(self, idx, color: str):
        log(f'Setting row {idx} to color: {color}')
        row = self.grid[idx]
        self._unset_colors = [seg.style for seg in row]
        y = idx
        for x in range(len(self.grid[y])):
            # self.grid[y][x] = Segment(self.grid[y][x].text, Style(color=color))
            self.set_color_at(x, y, color)








    def __len__(self):
        return len(self.grid)


    def __getitem__(self, idx):
        if isinstance(idx, int):
            return self.grid[idx]
        elif isinstance(idx, slice):
            start = idx.start if idx.start else 0
            stop = idx.stop if idx.stop else (len(self.grid) - 1)
            step = idx.step if idx.step else 1
            # if self.is_table:
            #     start = min(start + 1, len(self.grid) - 1)
            #     stop  = min(stop  + 1, len(self.grid) - 1)
            res = []
            for i in range(start, stop, step):
                res.append(self.grid[i])
            if self.is_table:
                res = [self.column_names, *res]
            return LinesRenderable(res, self.is_table)


    def __rich_console__(self, console: Console, options: ConsoleOptions):
        c_height = console.height
        end_pos = min(self.pos + c_height, self.height)
        if self.is_table:
            #compensate for column_names being the first row of self.grid
            yield make_table([name if isinstance(name, Segment) else str(name) for name in self.column_names], self.grid[self.pos:end_pos])
        else:
            for line in self.grid[self.pos:end_pos]:
                for seg in line:
                    yield seg
                yield Segment.line()

