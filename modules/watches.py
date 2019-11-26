import time
from functools import partial

from PIL import ImageFont

from modules import Module


class Watches(Module):
    def __init__(self, size, update_interval):
        super().__init__(size, update_interval)
        self._time_font = ImageFont.truetype("res/watches/digital-7 (mono).ttf", 90)
        self._date_font = ImageFont.truetype("res/watches/digital-7 (mono).ttf", 40)

    def _draw_text(self, xy_cb, text, font, fill):
        self._canvas.text(
            xy_cb(
                self._canvas.textsize(
                    text,
                    font=font
                )
            ),
            text,
            font=font,
            fill=fill
        )

    def _clear_image(self):
        self._canvas.rectangle((0, 0, self.size[0], self.size[1]), fill=255)

    def __center_text(self, xy, x):
        return (self.size[0] // 2 - xy[0] // 2, x)

    def redraw(self):
        self._clear_image()
        self._draw_text(partial(self.__center_text, x=5), time.strftime("%H:%M"), self._time_font, 0)
        self._draw_text(partial(self.__center_text, x=80), time.strftime("%d %b %Y"), self._date_font, 0)
