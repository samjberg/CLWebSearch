
class Entry:
    def __init__(self, text:str, color=''):
        if isinstance(text, Entry):
            self.text =  text.text
            self._color = text._color
        else:
            self.text  : str = text
            self._color : str = ''
            if color:
                if isinstance(color, str):
                    if color[0] == '[' and color.endswith(']'):
                        self._color = color
                    else:
                        self._color = f'[{color}]'

    def get_color(self):
        return self._color[1:-1]

    def set_color(self, col):
        if not col:
            self._color = '[gray]'
            return
        if not col[0] == '[':
            col = '[' + col
        if not col.endswith(']'):
            col += ']'
        self._color = col

    def __add__(self, other):
        if isinstance(other, Entry):
            text = self.text + other.text
            color = self._color if self._color == other._color else ''
            return Entry(text, color)
        elif isinstance(other, str):
            return Entry(self.text + other, self._color)
        raise TypeError(f'Error, {other} has incompatible type {type(other)} to add to Entry')

    def __mult__(self, other):
        if type(other) in [int, float]:
            return Entry(self.text * other, self._color)
        raise TypeError(f'Error, {other} has incompatible type {type(other)} to multiply to Entry')

    def __eq__(self, other):
        if isinstance(other, Entry):
            return (self.text == other.text) and (self._color == other._color)
        elif isinstance(other, str):
            return self.text == other
        return False

    def __str__(self):
        return self._color + self.text

    def __repr__(self):
        return self._color + self.text

    def __hash__(self):
        return hash(self._color + self.text)

    def __rich__(self):
        return self.__str__()

#Create a row (of Entry objects) by passing either a list of strings, or a list of 2-tuples of (str, str)
#where the 2nd string is the color.  The color must appear in COLOR_NAMES (must be a key in rich.color.ANSI_COLOR_NAMES)
