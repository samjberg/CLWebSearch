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
from parsehtml import parse_raw_html


console = Console()

class PageRow:
    def __init__(self, row: list[Segment]):
        self.row = row

    def __getitem__(self, idx):
        if isinstance(idx, int):
            return self.row[idx]
        if isinstance(idx, slice):
            start = idx.start
            stop = idx.stop if idx.stop else len(self.row)
            step = idx.step if idx.step else 1
            res = []
            for i in range(start, stop, step):
                res.append(self.row[i])
            return PageRow(res)
        raise TypeError(f'Error indexing/slicing RenderedPage, type must be int or slice, got: {type(idx)}')

    def __rich_console__(self, console: Console, options: ConsoleOptions):
        for seg in self.row:
            yield seg
            yield ' '
        # yield Segment.line()


class RenderedPage:
    def __init__(self, s: str):
        self.raw_text = s
        self.text = parse_raw_html(s)
        # self.grid = []
        self.grid = []
        for line in self.text.splitlines():
            # row = PageRow([Segment(part) for part in raw_line.split(' ')])
            self.grid.append(line)


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
            return PageRow(res)
        raise TypeError(f'Error indexing/slicing RenderedPage, type must be int or slice, got: {type(idx)}')

    def __len__(self):
        term_width, term_height = get_terminal_size()
        actual_lines = 0
        remainder = 0
        for line in self.grid:
            l = len(line)
            #get the current line length including remainder from previous line(s)
            curr_len = l + remainder
            if curr_len != 0:
                new_lines, remainder = divmod(term_width, curr_len)
                actual_lines += new_lines
        return actual_lines



    def __rich_console__(self, console: Console, options: ConsoleOptions):
        for line in self.text.splitlines():
            yield line
            yield Segment.line()
        # yield self.text
        # for line in self.grid:
        #     for seg in line:
        #         yield seg
        #     yield Segment('\n')


    def __str__(self):
        return self.text


