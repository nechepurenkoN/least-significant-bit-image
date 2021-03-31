from typing import Tuple, Iterator, Callable

from PIL import Image

from lsbencoder.exceptions import InvalidPixelChannelException


class PixelWrapper:
    def __init__(self, pixel: Tuple[int, int, int], callback: Callable):
        self.__pixel = list(pixel)
        self.__cb = callback

    def change_channel_value(self, channel: int, variation: int):
        if not 0 <= channel <= 2:
            raise InvalidPixelChannelException("Channel should be one of (0-R, 1-G, 2-B)")
        self.__pixel[channel] += variation

    def channel_value(self, channel: int) -> int:
        if not 0 <= channel <= 2:
            raise InvalidPixelChannelException("Channel should be one of (0-R, 1-G, 2-B)")
        return self.__pixel[channel]

    def save(self):
        self.__cb(tuple(self.__pixel))

    def __repr__(self) -> str:
        return self.__pixel.__repr__()


class SteganoImageWrapper:
    def __init__(self, path_to_image: str):
        self.__image = Image.open(path_to_image)

    def next_pixel_getter(self) -> Iterator[PixelWrapper]:
        provider = PixelsProvider(self.__image)
        yield from provider.get_flatten_pixels()

    def save(self, name: str):
        if not name.endswith(".png"):
            name = name + ".png"
        self.__image.save(name, format="png")

    def close(self):
        self.__image.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class PixelsProvider:
    def __init__(self, image: Image):
        self.__pixels = image.load()
        self.__width, self.__height = image.size

    def get_flatten_pixels(self) -> Iterator[PixelWrapper]:
        for x in range(self.__height):
            for y in range(self.__width):
                yield PixelWrapper(self.__pixels[y, x],
                                   lambda value, y=y, x=x: self.__pixels.__setitem__((y, x), value)
                                   )
