import os, sys, requests, rich, json
import keyboard

from rich import print as rprint
from rich.console import Console
from rich.live import Live
from rich.table import Table
from resulttable import COLOR_DICT, COLOR_NAMES, Entry, ResultTable
from time import sleep
from inscriptis import get_text



def remove_color_tags(s: str):
    if isinstance(s, Entry):
        entry = s
        s = entry.text
        if not s:
            print(f'NOT S')
            return entry
        while s.startswith('['):
            # log(f'in remove_color_tags while loop.  s:{s}')
            end_idx = s.find(']')
            if end_idx == -1:
                return s
            s = s[end_idx+1:]
        return s
    else:
        if not s:
            return s
        while s.startswith('['):
            end_idx = s.find(']')
            if end_idx == -1:
                return s
            s = s[end_idx+1:]
        return s



# def remove_color_tags(s: str):
#     while s.startswith('['):
#         end_idx = s.find(']')
#         if end_idx == -1:
#             return s
#         s = s[end_idx+1:]
#     return s


url = sys.argv[1]


print(url)
print(remove_color_tags(url))

