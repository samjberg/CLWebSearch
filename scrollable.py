import os
from logger import log

class Scrollable:
    def __init__(self, scroll_mult=1):
        self.pos = 0
        self.scroll_multiplier = scroll_mult
        self.height = 10000000

    #note this function is currently logging on every scroll event
    def scroll(self, n: int) -> None:
        prev_pos = self.pos
        term_height = os.get_terminal_size()[1]
        max_pos = self.height - term_height
        self.pos += n * self.scroll_multiplier
        if self.pos > max_pos:
            self.pos = max_pos - 1
        amount_scrolled = self.pos - prev_pos
        log(f'Scrolling {n} with multiplier of {self.scroll_multiplier} for a total of: {amount_scrolled}')





    def scroll_down(self, n: int) -> None:
        self.scroll(n)

    def scroll_up(self, n: int) -> None:
        self.scroll(-n)
        if self.pos < 0:
            self.pos = 0
