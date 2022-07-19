from enum import Enum

color = "background-color: rgba(13, 110, 253, {0})"


class Color(Enum):
    BUTTON_PRIMARY = color.format(.6)
    BUTTON_HOVER = color.format(.8)
    BUTTON_PRESSED = color.format(1)
