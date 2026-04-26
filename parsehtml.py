from bs4 import BeautifulSoup
from rich import inspect, print
from logger import log


# with open('page.html', 'rb') as f:
#     html_bytes = f.read()
#     html_text = html_bytes.decode(errors='replace')


def parse_raw_html(html_text: str) -> str:
    soup = BeautifulSoup(html_text, features='lxml')
    body: bs4.element.Tag = soup.find('body')
    btext = body.text
    while btext.count('\n\n') > 25:
        btext = btext.replace('\n\n', '\n')
    btext = btext.replace('\n\n', '\n')
    log(f'number of \\r\'s in btext: {btext.count('\r')}')
    return btext
