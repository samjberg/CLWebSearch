import os, sys, requests, rich, json
import keyboard
from rich import print as rprint
from rich.console import Console
from rich.live import Live
from rich.segment import Segment
from rich.table import Table
from rich.style import Style
from rich.text import Text
from resulttable import COLOR_DICT, COLOR_NAMES, Entry, ResultTable
from time import sleep
from parsehtml import parse_raw_html
from scrollable import Scrollable
from logger import log
from renderedpage import RenderedPage, PageRow


# def generate_table(column_names:list[str], rows=[], **kwargs) -> ResultTable:
#     table = ResultTable(column_names)
#     for name in column_names:
#         table.add_column(name)
#     for i in range(min(10, len(rows))):
#         row = rows[i]
#         rprint(f'row: {row}')
#         # try:
#         table.add_row(*row)
#         # except:
#         #     rprint(f'Unable to add {row} to table')
#     return table


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



console = Console()
with open('page.html', 'rb') as f:
    html_bytes = f.read()
    parsed_html = html_bytes.decode(errors='replace')
    # for line in f.readlines():
    #     if line.isascii():
    #         parsed_html += line.decode(
rendered_html = parse_raw_html(parsed_html)
# rprint(rendered_html)
# exit()

page = RenderedPage(parsed_html)
# scrollable = MyScrollable(page, console)
# rprint(scrollable)
# exit()


USER_AGENT = 'CLWebSearchAgent/0.1 (sjberg14@gmail.com) Python-requests/2.33.0'
#screens
RESLST_SCREEN = 'results_list_screen'
WEBPAGE_SCREEN = 'webpage_screen'


api_key = os.environ.get('BRAVE_API_KEY')
search_engine = 'brave'

curr_idx = 0
running = True
args = sys.argv[1:]
query : str = args[-1]
rows = []
res_url = ''
# curr_screen = RESLST_SCREEN
curr_screen = WEBPAGE_SCREEN


params = {
    "q": query
}

headers = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip",
    "User-Agent": USER_AGENT,
    "X-Subscription-Token": api_key
}

# resp = requests.get(req_url, params=params, headers=headers)
# results = resp.json()
start_idx = 0
highlight_color = '[yellow]'


# def save_html_file(html_text, fname='page.html'):
#     with open(fname, 'w') as f:
#         f.write(html_text)


# for i in range(len(results_list)):
#     result = results_list[i]
#     if i == curr_idx:
#         title = highlight_color + result['title']
#         url   = highlight_color + result['url']
#         desc  = highlight_color + result['description']
#     else:
#         title = result['title']
#         url = result['url']
#         desc = result['description']
#     rows.append([Segment(s) for s in [title, f'[blue]{url}', f'{desc}']])
#     rows.append([s for s in [title, f'[blue]{url}', f'{desc}']])


search_urls_dict = {'brave': 'https://api.search.brave.com/res/v1/web/search?q='}
req_url = search_urls_dict[search_engine]
with open('results.json', 'r') as f:
    results = json.load(f)

results_list : list[dict] = results['web']['results']

for _ in range(10):
    for result in results_list:
        rows.append([Text(result['title'], 'yellow'), Text(result['url'], 'blue'), Text(result['description'], 'red')])

# print(f'num results: {len(results_list)}')
# exit()

table = ResultTable(['Title', 'URL', 'Description'], title=f'Search Results for: {query}', rows=rows)
# x = int(sys.argv[1])
# y = int(sys.argv[2])


for i in range(min(len(table), 10)):
    print(f'actual height of row {i}: {table.get_row_height(console, i)}')

# exit()



# rprint(table)
# rprint(table.get_height(console))
#
#
# lines = console.render_lines(table)
# for line in lines:
#     for seg in line:
#         print(Text(seg.text, seg.style), end='')
#     # rprint(line)

# exit()


# scrollable = MyScrollable(table, console)
# live = Live(scrollable, auto_refresh=True, screen=True)

scrollable:Scrollable = None



def handle_keypress_j(e):
    global curr_idx, table, start_idx, scrollable, curr_screen
    curr_idx += 1
    # scrollable.scroll_down(1)
    if curr_screen == RESLST_SCREEN:
        table.highlight_row(curr_idx)#+ curr_offset)
        curr_pos_height = scrollable.get_height(scrollable.pos)
        screen_height = os.get_terminal_size()[1]
        scrollable_height = scrollable.get_height(up_to=curr_idx)# + curr_offset)
        log(f'screen_height: {screen_height}, scrollable_height: {scrollable_height}, curr_pos_height: {curr_pos_height}')
        if (screen_height - scrollable_height) < 3:
            row_height = table.get_row_height(console, curr_idx)# + curr_offset)
            scrollable.scroll_down(1)
            log(f'scrollable.pos: {scrollable.pos}')
        # for i in range(curr_idx + curr_offset):
        #     table.set_row_color(i, 'gray')
    else:
        scrollable.scroll(1)

    # if curr_screen == WEBPAGE_SCREEN:
        # start_idx += 50
    # for i in range(20):
    #     rprint(i)


def handle_keypress_k(e):
    global curr_idx, table, start_idx, scrollable, curr_screen
    curr_idx -= 1
    # scrollable.scroll_up(1)
    if curr_screen == RESLST_SCREEN:
        table.highlight_row(curr_idx)# + curr_offset)
        screen_height = os.get_terminal_size()[1]
        scrollable_height = scrollable.get_height(up_to=curr_idx)# + curr_offset)
        log(f'scrollable_height: {scrollable_height}\tscrollable.pos: {scrollable.pos}')
        if (screen_height - scrollable_height) < 3:
            row_height = table.get_row_height(console, curr_idx)# + curr_offset)
            scrollable.scroll_up(1)
        # for i in range(curr_idx+1, len(table)):
        #     table.set_row_color(i, 'gray')

    else:
        scrollable.scroll_up(1)




def stop_running(e):
    global running
    running = False

def handle_keypress_space(e):
    global table, running, live, alt_live, res_url, curr_screen

    entry = table.grid[curr_idx][1]
    res_url = table.grid[curr_idx][1]
    # print(f'url style for row {curr_idx}: {entry.style}')
    running = False


def handle_keypress_enter(e):
    global table, running, live, scrollable, alt_live, res_url, curr_screen
    row = table.get_row(curr_idx)
    log(f'in handle_keypress_enter.  row[1]:{row[1]}')
    res_url = remove_color_tags(str(row[1]))

    running=False
    curr_screen = WEBPAGE_SCREEN
    # log(f'running requests.get on url: {res_url}')
    # resp = requests.get(res_url)
    # with open('page.html', 'r') as f:
    #     rendered_html = f.read()
    # rendered_html = parse_raw_html(resp.text)
    # live.renderable = rendered_html




    # resp = requests.get('asdgdasgds')
    # running = False
    # rendered_html = parse_raw_html(resp.text)
    # table._table = table._table[0]
    # table.add_row([Entry(rendered_html)])
    # with open('rendered_html.txt', 'w') as f:
    #     f.write(rendered_html)
    # # alt_live = live
    # table._table = [['Page'], [Entry(rendered_html)]]
    # live = Live(rendered_html)
    # print(rendered_html)


keyboard.on_press_key('j', handle_keypress_j, True)
keyboard.on_press_key('k', handle_keypress_k, True)
keyboard.on_press_key('q', stop_running, True)
keyboard.on_press_key('space', handle_keypress_space, True)
keyboard.on_press_key('enter', handle_keypress_enter, True)




# scrollable = Scrollable(table)
# scrollable = Scrollable(table)
# table_live = Live(table_scrollable)

# scrollable = Scrollable(page)
# live = Live(scrollable, auto_refresh=True, refresh_per_second=4)
# term_height = os.get_terminal_size()[1]
# running = True
# with live:
#     while running:
#         live.update(scrollable, refresh=True)
# exit()



running = True
curr_screen = RESLST_SCREEN

# curl "https://api.search.brave.com/res/v1/web/search?q=artificial+intelligence" \
#   -H "X-Subscription-Token: YOUR_API_KEY"

if __name__ == '__main__':
    max_entries = 20
    alt_live = None

    scrollable = Scrollable(table)
    live = Live(scrollable, auto_refresh=True, refresh_per_second=4)
    term_height = os.get_terminal_size()[1]
    running = True
    with live:
        while running:
            live.update(scrollable, refresh=True)
    # exit()



    # resp = requests.get(req_url, params=params, headers=headers)
    # results : dict = resp.json()
    
    # if results:
    #     with open('results.json', 'w') as f:
    #         json.dump(results, f)
    #
    # if not results.get('web', {}).get('results'):
    #     rprint('Error: no results returned.  printing full json:')
    #     rprint(results)
    #     exit()


    

    # table = generate_table(['Title', 'URL', 'Description'], rows, show_lines=False)
    

    # rprint(table.table())
    # exit()

    
    # console.control()



    # exit()

    # live = Live(table.table(), refresh_per_second=4)
    # console.set_live(live)
    #
    # live.start(True)



    # with Live(table.table(), auto_refresh=True, screen=True) as live:
    # print(type(scrollable))
    # exit()
    # with live:
    #     while running:
    #         # print(type(scrollable))
    #         table.title=str(curr_idx)
    #         live.update(scrollable, refresh=True)
    #         # sleep(0.01)
    #         # live.refresh()
    #             # live.console.clear_live()
    # log('Reached the end of the with live block')


    #so fucking dumb.  I spent like 15 minutes trying to track down this error.
    #It turns out that it's literally just that... like because the key handling is being done separately, and asynchronously
    #the problem was that even though res_url was being set correctly, it was not being set until after the requests.get line
    #executed.  So.... we sleep for 0.1 seconds to solve that problem.  What an amazing solution lmao, so well thought out.
    sleep(0.1)
    # rprint(live.renderable)
    req_headers = {"User-Agent": USER_AGENT}
    curr_screen = WEBPAGE_SCREEN

    running = True

    # parsed_html = ''

    # print(f'res_url: {res_url}')
    # exit()

    # resp = requests.get(res_url, headers=req_headers)
    # rendered_html = parse_raw_html(resp.text)
    # # html_grid = [[Text(word) for word in line.split(' ')] for line in rendered_html.split('\n')]
    # page = RenderedPage(rendered_html)
    # scrollable = Scrollable(rendered_html, live)
    # live = Live(scrollable, auto_refresh=False, screen=True)
    # if (curr_screen == WEBPAGE_SCREEN):



    # with open('page.html', 'rb') as f:
    #     html_bytes = f.read()
    #     parsed_html = html_bytes.decode(errors='replace')
        # for line in f.readlines():
        #     if line.isascii():
        #         parsed_html += line.decode(
    # rendered_html = parse_raw_html(parsed_html)
    # page = RenderedPage(parsed_html)
    # lines = [Segment(line) for line in rendered_html.splitlines(keepends=True)]
    # live = Live(scrollable, auto_refresh=True, refresh_per_second=4)
    # term_height = os.get_terminal_size()[1]
    #
    # with live:
    #     while running:
    #         live.update(scrollable, refresh=True)
    #

    scrollable = Scrollable(page)
    live = Live(scrollable, auto_refresh=True, refresh_per_second=4)
    term_height = os.get_terminal_size()[1]
    running = True
    with live:
        while running:
            live.update(scrollable, refresh=True)
    exit()













