import os, sys, requests, rich, json
import keyboard

from rich import print as rprint
from rich.console import Console
from rich.live import Live
from rich.segment import Segment
from rich.table import Table
from resulttable import COLOR_DICT, COLOR_NAMES, Entry, ResultTable
from time import sleep
from inscriptis import get_text
from scrollable import Scrollable


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


logfile_path = 'log.txt'# = open('log.txt', 'a')
def log(s: str):
    with open(logfile_path, 'a') as logfile:
        print(s, end="\n", file=logfile)

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
curr_screen = RESLST_SCREEN


params = {
    "q": query
}

headers = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip",
    "User-Agent": USER_AGENT,
    "X-Subscription-Token": api_key
}

search_urls_dict = {'brave': 'https://api.search.brave.com/res/v1/web/search?q='}
req_url = search_urls_dict[search_engine]
# resp = requests.get(req_url, params=params, headers=headers)
# results = resp.json()
start_idx = 0

with open('results.json', 'r') as f:
    results = json.load(f)

results_list : list[dict] = results['web']['results']

highlight_color = '[yellow]'

def save_html_file(html_text, fname='page.html'):
    with open(fname, 'w') as f:
        f.write(html_text)


for i in range(len(results_list)):
    result = results_list[i]
    if i == curr_idx:
        title = highlight_color + result['title']
        url   = highlight_color + result['url']
        desc  = highlight_color + result['description']
    else:
        title = result['title']
        url = result['url']
        desc = result['description']

    rows.append([title, f'[blue]{url}', f'{desc}'])

table = ResultTable(['Title', 'URL', 'Description'], title=f'Search Results for: {query}', rows=rows)
live = Live(table.table(), auto_refresh=True, screen=True)
scrollable = Scrollable(live, str(table))


def handle_keypress_j(e):
    global curr_idx, table, start_idx, scrollable
    curr_idx += 1
    if curr_screen == RESLST_SCREEN:
        table.highlight_row(curr_idx)
        screen_height = os.get_terminal_size()[1]
        scrollable_height = scrollable.get_height(up_to=curr_idx)
        if (screen_height - scrollable_height) < 3:
            scrollable.scroll_down(1)
    else:
        scrollable.scroll_down(1)

    # if curr_screen == WEBPAGE_SCREEN:
        # start_idx += 50
    # for i in range(20):
    #     rprint(i)


def handle_keypress_k(e):
    global curr_idx, table, start_idx, scrollable
    curr_idx -= 1
    if curr_screen == RESLST_SCREEN:
        table.highlight_row(curr_idx)
        screen_height = os.get_terminal_size()[1]
        scrollable_height = scrollable.get_height(up_to=curr_idx)
        if (screen_height - scrollable_height) < 3:
            scrollable.scroll_up(1)
    else:
        scrollable.scroll_up(5)


# def handle_keypress_k(e):
#     global curr_idx, table, start_idx
#     # if curr_screen == RESLST_SCREEN:
#     curr_idx -= 1
#     table.highlight_row(curr_idx)
#     # else:
#     if curr_screen == WEBPAGE_SCREEN:
#         scrollable.scroll_up(5)
#         # start_idx = max(start_idx-50, 0)


def stop_running(e):
    global running
    running = False


def handle_keypress_enter(e):
    global table, running, live, alt_live, res_url, curr_screen
    row = table.get_row(curr_idx)
    log(f'in open_site.  row[1]:{row[1]}')
    res_url = remove_color_tags(row[1])
    # log(f'running requests.get on url: {res_url}')
    # resp = requests.get(res_url)
    with open('page.html', 'r') as f:
        rendered_html = f.read()
    # rendered_html = get_text(resp.text)
    live = Live(rendered_html, auto_refresh=False, screen=True)
    # live.renderable = rendered_html

    running=False
    curr_screen = WEBPAGE_SCREEN

    # resp = requests.get('asdgdasgds')
    # running = False
    # rendered_html = get_text(resp.text)
    # table._table = table._table[0]
    # table.add_row([Entry(rendered_html)])
    # with open('rendered_html.txt', 'w') as f:
    #     f.write(rendered_html)
    # # alt_live = live
    # table._table = [['Page'], [Entry(rendered_html)]]
    # live = Live(rendered_html)
    # print(rendered_html)



# curl "https://api.search.brave.com/res/v1/web/search?q=artificial+intelligence" \
#   -H "X-Subscription-Token: YOUR_API_KEY"

if __name__ == '__main__':
    max_entries = 10
    alt_live = None

    keyboard.on_press_key('j', handle_keypress_j, True)
    keyboard.on_press_key('k', handle_keypress_k, True)
    keyboard.on_press_key('q', stop_running, True)
    keyboard.on_press_key('enter', handle_keypress_enter, True)


    # resp = requests.get(req_url, params=params, headers=headers)
    # results : dict = resp.json()
    
    if results:
        with open('results.json', 'w') as f:
            json.dump(results, f)

    if not results.get('web', {}).get('results'):
        rprint('Error: no results returned.  printing full json:')
        rprint(results)
        exit()


    

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
    with live:
        while running:
            table.title=str(curr_idx)
            live.update(table, refresh=True)
            # sleep(0.01)
            # live.refresh()
                # live.console.clear_live()
    log('Reached the end of the with live block')


        #so fucking dumb.  I spent like 15 minutes trying to track down this error.
        #It turns out that it's literally just that... like because the key handling is being done separately, and asynchronously
        #the problem was that even though res_url was being set correctly, it was not being set until after the requests.get line
        #executed.  So.... we sleep for 0.1 seconds to solve that problem.  What an amazing solution lmao, so well thought out.
    sleep(0.1)
    # rprint(live.renderable)
    req_headers = {"User-Agent": USER_AGENT}

    running = True

    # parsed_html = ''

    # if (curr_screen == WEBPAGE_SCREEN):
    # resp = requests.get(res_url, headers=req_headers)
    with open('page.html', 'rb') as f:
        html_bytes = f.read()
        parsed_html = html_bytes.decode(errors='replace')
        # for line in f.readlines():
        #     if line.isascii():
        #         parsed_html += line.decode(

    page_text = get_text(parsed_html)

    lines = [Segment(line) for line in page_text.splitlines(keepends=True)]

    # parsed_html = get_text(resp.text)
    live = Live(page_text)
    scrollable = Scrollable(live, lines)
    # save_html_file(parsed_html)
    term_height = os.get_terminal_size()[1]

    live = Live(page_text, auto_refresh=True, screen=True)
    with live:
        while running:
            live.update(scrollable[curr_idx: curr_idx + term_height], refresh=True)

    # print(f'Selected url: {res_url}')















