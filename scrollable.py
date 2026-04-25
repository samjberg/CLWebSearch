import os
from rich import inspect, print
from rich.console import Console, ConsoleOptions, RenderableType
from rich.live import Live
from rich.layout import Layout
from rich.segment import Segment
from rich.text import Text
from rich.style import Style
from resulttable import ResultTable
from math import ceil



# running = True

class Scrollable:
    def __init__(self, live: Live, val):
        self.layout = Layout()
        self.console = live.console
        self.pos = 0
        self.live = live
        if isinstance(val, str):
            n_rows = os.get_terminal_size()[1] #number of rows in terminal
            self.segments = [Segment(line) for line in val.splitlines()]
            self.text = ''
        elif isinstance(val, list):
            self.segments: list[Segment] = []
            for line in val:
                if isinstance(line, str):
                    self.segments.append(Segment(line))
                elif isinstance(line, Segment):
                    self.segments.append(line)
                elif isinstance(line, list):
                    if not all([isinstance(part, str) or isinstance(part, Segment) for part in line]):
                        badtype = None
                        for part in line:
                            if not isinstance(part, str) and not isinstance(part, Segment):
                                badtype = type(part)
                                break
                        raise TypeError(f'Error in Scrollable constructor.  2d list must contain only str and/or Segment.  Found part with type: {type(badtype)}')
                    if all([isinstance(part, str) for part in line]):
                        text = '\t'.join(line)
                        self.segments.append(Segment(text))
                    elif all([isinstance(part, Segment) for part in line]):
                        combined_segment = Segment('')
                        for part in line:
                            combined_segment += part
                        self.segments.append(combined_segment)

                elif isinstance(line, Segment):
                    self.segments.append(line)
                else:
                    raise TypeError(f'Error, line from val has type {type(line)}.  Must be str or Segment.  Line: {line}')
            self.text = '\n'.join([seg.text for seg in self.segments])
        elif isinstance(val, ResultTable):
            self.text = str(val)
            self.segments = [Segment(part) for part in self.text.splitlines()]
        else:
            raise TypeError(f'Error in Scrollable constructor: val has type: {type(val)}, it must be either str, list[str], list[list[str]], Segment, list[Segment], or list[list[Segment]]')

        # seg = self.segments[0]
        # Segment.get_shape([self.segments])


    def to_segments_lines(self, up_to:int = -1) -> list[list[Segment]]:
        if up_to == -1:
            up_to = len(self.segments)
        lines: list[list[Segment]] = []
        for seg in self.segments[:up_to]:
            sub_segments = [Segment(part, seg.style) for part in seg.text.split(' ')]
            lines.append(sub_segments)
        return lines

    def get_height(self, up_to:int = -1) -> int:
        if up_to == -1:
            up_to = len(self.segments)
        return Segment.get_shape(self.to_segments_lines(up_to))[1]




    def scroll(self, n: int):
        num_lines = len(self.segments)
        num_lines_terminal = os.get_terminal_size()[1]
        #max_idx is determined by seeing how many lines fit on the terminal, and going that many
        #lines back from the end of self.segments (which each segment represents 1 line)
        max_idx = num_lines - num_lines_terminal
        #this max and min call ensures that self.pos stays between 0 and max_idx
        self.pos = max(min(self.pos + n, max_idx), 0)
        with open('log.txt', 'a') as log:
            log.write(f'scrolling {n}')
        return True

    def scroll_down(self, n: int):
        if n <= 0:
            return
        self.scroll(n)

    def scroll_up(self, n: int):

        if n <= 0:
            return
        self.scroll(-n)

    def __getitem__(self, idx):
        if isinstance(idx, int):
            seg = self.segments[idx]
            return Scrollable(self.live, seg.text)
        elif isinstance(idx, slice):
            start = idx.start
            stop = idx.stop if idx.stop else len(self.segments)
            step = idx.step if idx.step else 1
            segs = []
            for i in range(start, stop, step):
                segs.append(self.segments[i])
            renderable = '\n'.join([seg.text for seg in segs])
            live = Live(renderable, console=self.console, refresh_per_second=self.live.refresh_per_second, auto_refresh=self.live.auto_refresh)
            return Scrollable(live, segs)




    def __setitem__(self, idx, val):
        if isinstance(val, Segment):
            self.segments[idx] = val
        elif isinstance(val, Text):
            if isinstance(val.style, Style):
                self.segments[idx] = Segment(' '.join(val._text), style=val.style)
            else:
                self.segments[idx] = Segment(' '.join(val._text))
        elif isinstance(val, str):
            self.segments[idx] = Segment(val)
        else:
            raise TypeError(f'To set item in Scrollable type must be Segment|Text|str, got: {type(val)}')




    def __rich_console__(self, console: Console, options: ConsoleOptions):
        terminal_width, num_lines_terminal = os.get_terminal_size()
        start = self.pos
        end = min(start + num_lines_terminal, len(self.segments))
        for seg in self.segments[start:end]:
            yield seg.text

    def __repr__(self):
        terminal_width, num_lines_terminal = os.get_terminal_size()
        start = self.pos
        end = min(start + num_lines_terminal, len(self.segments))
        return '\n'.join([seg.text for seg in self.segments[start:end]])

    def __str__(self):
        terminal_width, num_lines_terminal = os.get_terminal_size()
        start = self.pos
        end = min(start + num_lines_terminal, len(self.segments))
        return '\n'.join([seg.text for seg in self.segments[start:end]])
        # return str(self.__rich_console__(self.console, self.console.options))


#
# lst = [['hello', 'there'], ['aaa', 'bbb']]
#
#
# scr = Scrollable(Live(), lst)


# if __name__ == '__main__':
#
#     with open('page.html', 'r') as f:
#         text = f.read()
#
#     live = Live(text, auto_refresh=True, screen=True)
#     scrollable = Scrollable(live, text)
#
#     with live:
#         while running:
#             live.update(
#
#
#
#
#
#
#
#
#
#
#
#
