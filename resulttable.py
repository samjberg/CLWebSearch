from rich.console import RenderableType
from rich.table import Table
from rich.color import ANSI_COLOR_NAMES as COLOR_DICT
from typing import Union
from entry import Entry

Renderable = Union[str, list[str]]

COLOR_NAMES = list(COLOR_DICT.keys())

#it IS allowed to mix both basic strings and string tuples within a single list, to give color to only certain entries
def create_row(basic_row, default_color='') -> list:
    row = []
    for entry in basic_row:
        if isinstance(entry, str):
            row.append(Entry(entry, default_color))
        elif isinstance(entry, tuple):
            if len(entry) == 2:
                text, color = entry
                row.append(Entry(text, color))
            else:
                row.append(Entry(entry[0], default_color))
        else:
            raise TypeError(f'Error, entry: {entry} in basic_row has invalid type: {type(entry)}.  Must be str or tuple')
    return row






class ResultTable:
    def __init__(self, column_names:list[str], title:str='', rows:list[list[Entry]]|None=[]):
        self.column_names:list[str] = column_names
        self._table = []
        self.title = title
        self.highlighted_row = 0

        # self.columns = self.table.columns
        if rows:
            for row in rows:
                if all([isinstance(x, Entry) for x in row]):
                    self._table.append(row)
                else:
                    row = [entry if isinstance(entry, Entry) else Entry(entry) for entry in row]
                    self._table.append(row)


    def get_row(self, row_index: int):
        return self._table[row_index]

    def add_row(self, row:list) -> None:
        self._table.append(create_row(row))

    def update_entry(self, row: int, col:str|int, val: str):
        col_index = self.column_names.index(col) if isinstance(col, str) else col
        self._table[row][col_index] = val

    def update_row(self, row_idx: int, row: list[Entry]):
        if not all([isinstance(entry, Entry) for entry in row]):
            default_color:str = self._table[row_idx][0].color
            row = create_row(row, default_color)
        self._table[row_idx] = row

    def set_row_color(self, row_idx: int, color: str):
        for entry in self._table[row_idx]:
            entry.set_color(color)

    def highlight_row(self, row_idx, color='yellow'):
        for idx, row in enumerate(self._table):
            if idx == row_idx:
                continue
            if all([entry.get_color() == color for entry in row]):
                self.set_row_color(idx, '')
        self.set_row_color(row_idx, color)
        self.highlighted_row = row_idx




    def __len__(self):
        return len(self._table)



    def __rich__(self) -> RenderableType:
        table = Table(title=self.title)
        for column_name in self.column_names:
            table.add_column(column_name)
        for row in self._table:
            table.add_row(*row)
        return table

    def __repr__(self):
        return str(self.__rich__())
    
    def __str__(self):
        return self.__repr__()


    def table(self) -> RenderableType:
        return self.__rich__()
