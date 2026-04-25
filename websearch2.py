import os, sys, requests, rich, json
import keyboard

from rich import print as rprint
from rich.console import Console
from rich.live import Live
from rich.table import Table
from resulttable import COLOR_DICT, COLOR_NAMES, Entry, ResultTable
from time import sleep
from inscriptis import get_text

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





api_key = os.environ.get('BRAVE_API_KEY')
search_engine = 'brave'

curr_idx = 0
running = True
args = sys.argv[1:]
query : str = args[-1]
rows = []
res_url = ''


params = {
    "q": query
}

headers = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip",
    "X-Subscription-Token": api_key
}

search_urls_dict = {'brave': 'https://api.search.brave.com/res/v1/web/search?q='}
req_url = search_urls_dict[search_engine]
resp = requests.get(req_url, params=params, headers=headers)
results = resp.json()


results_list : list[dict] = results['web']['results']

highlight_color = '[yellow]'


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


def increment_curr_idx(e):
    global curr_idx, table
    curr_idx += 1
    table.highlight_row(curr_idx)
    # for i in range(20):
    #     rprint(i)


def decrement_curr_idx(e):
    global curr_idx, table
    curr_idx -= 1
    table.highlight_row(curr_idx)


def stop_running(e):
    global running
    running = False


def open_site(e):
    global table, running, live, alt_live, res_url
    running=False
    row = table.get_row(curr_idx)
    log(f'in open_site.  row[1]:{row[1]}')
    res_url = remove_color_tags(row[1])
    log(f'running requests.get on url: {res_url}')
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

    keyboard.on_press_key('j', increment_curr_idx, True)
    keyboard.on_press_key('k', decrement_curr_idx, True)
    keyboard.on_press_key('q', stop_running, True)
    keyboard.on_press_key('enter', open_site, True)


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

    
    console.control()



    # exit()

    # live = Live(table.table(), refresh_per_second=4)
    # console.set_live(live)
    #
    # live.start(True)

    live = Live(table.table(), auto_refresh=True, screen=True)

    # with Live(table.table(), auto_refresh=True, screen=True) as live:
    with live:
        while running:
            table.title=str(curr_idx)
            live.update(table)
            sleep(0.01)
            live.refresh()
            # live.console.clear_live()

    #so fucking dumb.  I spent like 15 minutes trying to track down this error.
    #It turns out that it's literally just that... like because the key handling is being done separately, and asynchronously
    #the problem was that even though res_url was being set correctly, it was not being set until after the requests.get line
    #executed.  So.... we sleep for 0.1 seconds to solve that problem.  What an amazing solution lmao, so well thought out.
    sleep(0.1)

    # print(f'Selected url: {res_url}')
    resp = requests.get(res_url)
    parsed_html = get_text(resp.text)
    print(parsed_html)




































