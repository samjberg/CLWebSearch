import os
from rich import inspect, print
from rich.console import Console, ConsoleOptions, RenderableType
from rich.live import Live
from rich.layout import Layout
from rich.segment import Segment
from rich.text import Text
from rich.style import Style
from resulttable import ResultTable
from renderedpage import RenderedPage
from math import ceil
from logger import log


# running = True

class Scrollable:
    '''A helpful class which basically wraps a RenderableType and also makes it scrollable.
       This class itself is a RenderableType (it implements __rich_console__), and so can literally be used to wrap other
       RenderableType's

            `val`: A RenderableType, or a 1-2 dimensional list of RenderableType. This is the value to wrap.
    '''
    def __init__(self, val):
        live = Live()
        self.val = val
        self.live = live
        self.console = live.console
        self.layout = Layout()
        self.pos = 0
        self.height = -1
        self.segments = []
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
                    if not all([isinstance(part, str) or isinstance(part, Segment) or isinstance(part, Text) for part in line]):
                        badtype = None
                        for part in line:
                            if not isinstance(part, str) and not isinstance(part, Segment) and not isinstance(part, Text):
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
                    elif all([isinstance(part, Text) for part in line]):
                        for _ in range(10):
                            print('IN THIS ELIF BLOCK')
                        combined_segment = Text('')
                        for part in line:
                            combined_segment += Segment(str(part), part.style)

                elif isinstance(line, Segment):
                    self.segments.append(line)
                else:
                    raise TypeError(f'Error, line from val has type {type(line)}.  Must be str or Segment.  Line: {line}')
            self.text = '\n'.join([seg.text for seg in self.segments])
        elif isinstance(val, ResultTable):
            self.height = val.get_height(self.console)
            self.text = str(val)
            for row in val.grid:
                for entry in row:
                    if isinstance(entry, Segment):
                        self.segments.append(entry)
                    elif isinstance(entry, str):
                        self.segments.append(Segment(entry))
                    elif isinstance(entry, Text):
                        self.segments.append(Segment(str(entry), entry.style))
                    else:
                        raise TypeError(f'Error, ResultTable contained type other than str or Segment.  Got: {type(entry)}')
            # self.segments = [Segment(part) for part in val.grid]
            log(f'Creating scrollable with: {len(self.segments)} total segments')
        elif isinstance(val, RenderedPage):
            self.segments = [Segment(line) for line in val.grid]
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
        if self.height != -1:
            return self.height
        if up_to == -1:
            up_to = len(self.segments)
        screen_width = os.get_terminal_size()[0]
        total_length = 0
        total_height = 0
        for line in self.segments:
            # text = ' '.join([seg for seg in line])
            text = line.text
            log(f'segment: {text}')
            num_newlines = text.count('\n')
            num_tabs = text.count('\t')
            #this line is calculating the total linear length of text.  It takes the basic length (len(text)), and then
            #subtracts the number of newlines and the number of tabs (because they will both be dealt with specially).
            #The tab handling is then done by the 4*num_tabs, making every tab count as length 4, but without overcounting
            #because we removed the actual tab itself (otherwise we would be counting tabs as 5 spaces)
            l = len(text) - num_newlines  - num_tabs + (4*num_tabs)
            #handle the newlines specially by directly adding the number of them to total_height, since each newline
            #causes.... a new line.  Thus increasing the height by 1 per newline
            total_height += 1 + num_newlines
            total_length += l

        #now handle converting the rest of the counted length into height, and add it to total_height
        total_height += total_length // screen_width
        return total_height






        # return Segment.get_shape(self.to_segments_lines(up_to))[1]




    def scroll(self, n: int):
        num_lines_terminal = os.get_terminal_size()[1]
        if isinstance(self.val, ResultTable):
            row_height = self.val.get_row_height(self.console, self.pos)
            num_lines = len(self.val)
            max_idx = num_lines - num_lines_terminal
            self.pos = max(min(self.pos + (n * row_height), max_idx), 0)
        else:
            num_lines = len(self.segments)
            #max_idx is determined by seeing how many lines fit on the terminal, and going that many
            #lines back from the end of self.segments (which each segment represents 1 line)
            max_idx = num_lines - num_lines_terminal
            lines_per_scroll = 5
            #this max and min call ensures that self.pos stays between 0 and max_idx
            self.pos = max(min(self.pos + (n*lines_per_scroll), max_idx), 0)
            with open('log.txt', 'a') as log:
                log.write(f'scrolling {n}')

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
            return Scrollable(seg.text)
        elif isinstance(idx, slice):
            start = idx.start
            stop = idx.stop if idx.stop else len(self.segments)
            step = idx.step if idx.step else 1
            segs = []
            for i in range(start, stop, step):
                segs.append(self.segments[i])
            renderable = '\n'.join([seg.text for seg in segs])
            live = Live(renderable, console=self.console, refresh_per_second=self.live.refresh_per_second, auto_refresh=self.live.auto_refresh)
            return Scrollable(segs)




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
        if isinstance(self.val, ResultTable):
            table = self.val.get_table()
            lines = console.render_lines(table)
            end_pos = min(len(lines), self.pos + console.height)
            for line in lines[self.pos:end_pos]:
                for seg in line:
                    yield seg
                yield Segment.line()
        else:
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

