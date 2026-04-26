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
from logger import log
from entry import Entry


# running = True

class Scrollable:
    '''A helpful class which basically wraps a RenderableType and also makes it scrollable.
       This class itself is a RenderableType (it implements __rich_console__), and so can literally be used to wrap other
       RenderableType's

            `val`: A RenderableType, or a 1-2 dimensional list of RenderableType. This is the value to wrap.
    '''
    def __init__(self, val, live:Live|None=None):
        if isinstance(val, ResultTable):

        pass

        # seg = self.segments[0]
        # Segment.get_shape([self.segments])



