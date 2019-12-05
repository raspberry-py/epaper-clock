import time
from functools import partial

from PIL import ImageFont

from modules import Module


class Watches(Module):
    def __init__(self, size):
        super().__init__(size)
        self._time_font = ImageFont.truetype("res/watches/digital-7 (mono).ttf", 90)
        self._date_font = ImageFont.truetype("res/watches/digital-7 (mono).ttf", 40)

    def _clear_image(self):
        self._canvas.rectangle((0, 0, self.size[0], self.size[1]), fill=255)

    def _center_text(self, xy, y):
        return (self.size[0] // 2 - xy[0] // 2, y)

    def redraw(self):
        super().redraw()
        self._draw_text(partial(self._center_text, y=5), time.strftime("%H:%M"), self._time_font, 0)
        self._draw_text(partial(self._center_text, y=80), time.strftime("%d %b %Y"), self._date_font, 0)
