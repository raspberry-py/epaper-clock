from datetime import datetime

from PIL import Image, ImageDraw


class Module:
    def __init__(self, size, update_interval):
        self._size = size
        self._update_interval = update_interval
        self._last_update = datetime.min
        self._image = Image.new("1", size, 255)
        self._canvas = ImageDraw.Draw(self._image)

    def redraw(self):
        raise NotImplementedError("Not implemented")

    def update(self):
        t = datetime.now()

        if (t - self._last_update).seconds >= self._update_interval:
            self._last_update = t
            self.redraw()

    @property
    def size(self):
        return self._size

    @property
    def image(self):
        return self._image
