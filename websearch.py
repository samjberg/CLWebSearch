import os, sys, requests, keyboard, json
from keyboard import KeyboardEvent
from rich import print, inspect
# from rich import inspect
from rich.text import Text
from rich.live import Live
from rich.console import Console, ConsoleOptions, RenderableType
from linesrenderable import LinesRenderable
from parsehtml import parse_raw_html
from logger import log
from selectabletable import SelectableTable



def handle_keypress_j(e):
    global scrollable, screen_idx
    buffer = 5
    max_height = console.height - buffer
    if scrollable == table:
        scrollable_height = scrollable.get_height(scrollable.pos, screen_idx+1)
        log(f'scrollable_height: {scrollable_height}, max_height: {max_height}')
        if (scrollable_height+5) > max_height:
            scrollable.scroll_down(15)
        else:
            screen_idx += 1
        scrollable.move_selection_down(1)
    else:
        scrollable.scroll_down(1)

def handle_keypress_k(e):
    global scrollable, screen_idx
    buffer = 5
    min_height = console.height - buffer
    if scrollable == table:
        scrollable_height = scrollable.get_height(scrollable.pos, screen_idx-1)
        log(f'scrollable_height: {scrollable_height}, max_height: {min_height}')
        if (scrollable_height-5) < min_height:
            scrollable.scroll_up(15)
        else:
            screen_idx -= 1
        scrollable.move_selection_up(1)
    else:
        scrollable.scroll_up(1)


# def handle_keypress_j(e):
#     global scrollable, screen_idx, table
#     #screen_idx is the index ON SCREEN, so literally a number 0-N where N is the number of table rows currently on screen
#     if scrollable == table:
#         buffer = 5
#         c_height = console.height
#         #full height of scrollable up to curr_idx, INCLUDING all offscreen rows from the start
#         full_scrollable_height = table.get_height(end=scrollable.curr_idx)
#         #the height of the portion of scrollable from the start of the screen to curr_idx
#         screen_start_idx = curr_idx - screen_idx
#         before_height = table.get_height(screen_start_idx, curr_idx)
#         #the height of the portion of scrollable from curr_idx to end of screen
#         after_height = c_height - before_height
#         if screen_idx > 25:
#             table.scroll_down(1)
#     else:
#         pass
#
#
#
#
#
#
#
# def handle_keypress_k(e):
#     global scrollable, screen_idx
#     buffer = 5
#     min_height = console.height - buffer
#     if scrollable == table:
#         scrollable_height = scrollable.get_height(scrollable.pos, screen_idx-1)
#         log(f'scrollable_height: {scrollable_height}, max_height: {min_height}')
#         if (scrollable_height-5) < min_height:
#             scrollable.scroll_up(15)
#         else:
#             screen_idx -= 1
#         scrollable.move_selection_up(1)
#     else:
#         scrollable.scroll_up(1)





# def handle_keypress_k(e):
#     global scrollable
#     scrollable.scroll_up(1)


def handle_keypress_q(e):
    global running
    running = False

def handle_keypress_space(e):
    global scrollable, scrollables, scrollable_idx, live
    scrollable_idx = (scrollable_idx+1) % 2
    scrollable = scrollables[scrollable_idx]
    live.update(scrollable)

def handle_keypress_0(e: KeyboardEvent):
    line = scrollable.grid[0]
    log(f'{line[0].style}, {line[1].style}, {line[2].style}')

def handle_keypress_1(e: KeyboardEvent):
    line = scrollable.grid[1]
    log(f'{line[0].style}, {line[1].style}, {line[2].style}')


def handle_keypress_2(e: KeyboardEvent):
    line = scrollable.grid[2]
    log(f'{line[0].style}, {line[1].style}, {line[2].style}')

def handle_keypress_3(e: KeyboardEvent):
    line = scrollable.grid[3]
    log(f'{line[0].style}, {line[1].style}, {line[2].style}')

def handle_keypress_4(e: KeyboardEvent):
    line = scrollable.grid[4]
    log(f'{line[0].style}, {line[1].style}, {line[2].style}')

def handle_keypress_5(e: KeyboardEvent):
    line = scrollable.grid[5]
    log(f'{line[0].style}, {line[1].style}, {line[2].style}')


def handle_keypress_6(e: KeyboardEvent):
    line = scrollable.grid[6]
    log(f'{line[0].style}, {line[1].style}, {line[2].style}')



keyboard.on_press_key('j', handle_keypress_j, True)
keyboard.on_press_key('k', handle_keypress_k, True)
keyboard.on_press_key('q', handle_keypress_q, True)
keyboard.on_press_key('space', handle_keypress_space, True)
# keyboard.on_press_key('0', handle_keypress_0, True)
# keyboard.on_press_key('1', handle_keypress_1, True)
# keyboard.on_press_key('2', handle_keypress_2, True)
# keyboard.on_press_key('3', handle_keypress_3, True)
# keyboard.on_press_key('4', handle_keypress_4, True)
# keyboard.on_press_key('5', handle_keypress_5, True)
# keyboard.on_press_key('6', handle_keypress_6, True)
# keyboard.on_press(handle_keypress, True)
# keyboard.on_press_key('enter', handle_keypress_enter, True)


x = 5
curr_idx = 0
screen_idx = 0
running = True

if __name__ == '__main__':
    with open('./results.json', 'r') as f:
        results_dict = json.load(f)
    results_list : list[dict] = results_dict['web']['results']
    rows = [[Text('Title'), Text('URL'), Text('Description')]]
    for _ in range(10):
        for _ in range(10):
            for result in results_list:
                rows.append([Text(result['title'], 'yellow'), Text(result['url'], 'blue'), Text(result['description'], 'red')])


    table = SelectableTable(rows)
    #
    # for line in table.grid:
    #     print(type(line[0][1]))
    # exit()
    #


    # table = LinesRenderable(rows, as_table=True)



    with open('page.html', 'rb') as f:
        text_bytes = f.read()
        raw_html = text_bytes.decode(errors='replace')

    parsed_html = parse_raw_html(raw_html)
    page_lines = parsed_html.splitlines()
    page = LinesRenderable(page_lines, scroll_mult=5)


    scrollables = [table, page]
    scrollable_idx = 0
    scrollable = scrollables[scrollable_idx]

    for i in range(10):
        scrollable.set_row_color(i, 'green')



    console = Console()

    i = 0
    live = Live(scrollable, console=console, screen=True, auto_refresh=True, refresh_per_second=4)
    with live:
        while running:
            live.update(scrollable, refresh=True)
            # log(f'{i}', end = ' ')
            # if i % 100 == 0:
            #     log('\n')
            # i += 1




