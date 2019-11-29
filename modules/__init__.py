from datetime import datetime

from PIL import Image, ImageDraw


class Module:
    def __init__(self, size):
        self._size = size
        self._last_update = datetime.min
        self._image = Image.new("1", size, 255)
        self._canvas = ImageDraw.Draw(self._image)

    def redraw(self):
        raise NotImplementedError("Not implemented")

    @property
    def size(self):
        return self._size

    @property
    def image(self):
        return self._image
