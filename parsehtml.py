from bs4 import BeautifulSoup
from bs4.element import Tag
from rich import inspect, print
from logger import log


# with open('page.html', 'rb') as f:
#     html_bytes = f.read()
#     html_text = html_bytes.decode(errors='replace')


def parse_raw_html(html_text: str) -> str:
    soup = BeautifulSoup(html_text, features='lxml')
    body: Tag = soup.find('body')
    btext = body.text
    while btext.count('\n\n') > 25:
        btext = btext.replace('\n\n', '\n')
    btext = btext.replace('\n\n', '\n')
    log(f'number of \\r\'s in btext: {btext.count('\r')}')
    return btext




class HTMLParser:
    def __init__(self, html_text):
        self.soup = soup =  BeautifulSoup(html_text, features='lxml')
        body_tag: Tag = Tag(soup.find('body'))
        self.body = body_tag.text if body_tag else ''
