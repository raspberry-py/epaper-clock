from datetime import datetime

from PIL import Image, ImageDraw


class Module:
    def __init__(self, size):
        self._size = size
        self._last_update = datetime.min
        self._image = Image.new("1", size, 255)
        self._canvas = ImageDraw.Draw(self._image)

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

    def redraw(self):
        self._canvas.rectangle((0, 0, self.size[0], self.size[1]), fill=255)

    @property
    def size(self):
        return self._size

    @property
    def image(self):
        return self._image
