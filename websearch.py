import os, sys, requests
from rich import print
from rich.console import Console
from rich.live import Live
from rich.table import Table

def generate_table(column_names:list[str]=[]) -> Table:
    table = Table()
    for name in column_names:
        table.add_column(name)
    return table


console = Console()



api_key = os.environ.get('BRAVE_API_KEY')
search_engine = 'brave'
print(api_key)



search_urls_dict = {'brave': 'https://api.search.brave.com/res/v1/web/search?q='}

# curl "https://api.search.brave.com/res/v1/web/search?q=artificial+intelligence" \
#   -H "X-Subscription-Token: YOUR_API_KEY"

if __name__ == '__main__':
    args = sys.argv[1:]
    query : str = args[-1]
    params = {
        "q": query
    }

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key
    }

    table = generate_table(['Title', 'URL', 'Description'])
    max_entries = 10


    req_url = search_urls_dict[search_engine]
    resp = requests.get(req_url, params=params, headers=headers)
    results : dict = resp.json()

    if not results.get('web', {}).get('results'):
        print('Error: no results returned.  Printing full json:')
        print(results)
        exit()

    results_list : list[dict] = results['web']['results']

    with Live(table, refresh_per_second=4) as live:
        for i in range(min(10, len(results_list))):
            result = results_list[i]
            title = result['title']
            url = result['url']
            desc = result['description']
            table.add_row(title, f'[blue]{url}', f'[yellow]{desc}')



































