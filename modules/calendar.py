import time
from datetime import date

from PIL import Image, ImageFont

from modules import Module


class Calendar(Module):
    def __init__(self, size):
        super().__init__(size)
        self._seasons = [self._load_pic(s) for s in ("winter", "spring", "summer", "autumn")]
        self._date_font = ImageFont.truetype("res/calendar/SlimThinPixelettes-y5Y3.ttf", 30)
        self._day_font = ImageFont.truetype("res/calendar/ComputerPixel7-mnL2.ttf", 40)
        self._time_font = ImageFont.truetype("res/calendar/digital-7 (mono).ttf", 26)

    @staticmethod
    def _load_pic(name):
        img = Image.open(open(f"../res/calendar/{name}.png", "rb"))
        img.thumbnail((110, 110))
        return img

    def _clear_image(self):
        self._canvas.rectangle((0, 0, self.size[0], self.size[1]), fill=255)

    def _get_season_pic(self):
        return self._seasons[(date.today().month // 3) % 4]

    def redraw(self):
        super().redraw()
        self._image.paste(self._get_season_pic(), (-11, 5))
        self._draw_text(lambda _: (242 - _[0], 20), time.strftime("%B %d"), self._date_font, 0)
        self._draw_text(lambda _: (240 - _[0], 45), time.strftime("%A"), self._day_font, 0)
        self._draw_text(lambda _: (239 - _[0], 80), time.strftime("%H:%M"), self._time_font, 0)
