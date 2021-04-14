import abc
from abc import ABC
from typing import Tuple, Iterator

from PIL import Image
from PIL.PyAccess import PyAccess

from lsbencoder.exceptions import InvalidPixelChannelException


class PixelWrapper:
    def __init__(self, pixel: Tuple[int, int, int], position: Tuple[int, int]):
        self.__pixel = list(pixel)
        self.__position = position

    def change_channel_value(self, channel: int, variation: int):
        if not 0 <= channel <= 2:
            raise InvalidPixelChannelException("Channel should be one of (0-R, 1-G, 2-B)")
        self.__pixel[channel] += variation

    def channel_value(self, channel: int) -> int:
        if not 0 <= channel <= 2:
            raise InvalidPixelChannelException("Channel should be one of (0-R, 1-G, 2-B)")
        return self.__pixel[channel]

    def unpack(self):
        return self.__position, tuple(self.__pixel)

    def __repr__(self) -> str:
        return self.__pixel.__repr__()


class PixelsProvider:
    @abc.abstractmethod
    def get_iterator(self, pixels: PyAccess, width: int, height: int) -> Iterator[PixelWrapper]:
        raise NotImplementedError


class NaturalOrderPixelsProvider(PixelsProvider, ABC):
    def get_iterator(self, pixels: PyAccess, width: int, height: int) -> Iterator[PixelWrapper]:
        for x in range(height):
            for y in range(width):
                yield PixelWrapper(pixels[y, x], (y, x))


class LSBImageWrapper:
    def __init__(self, path_to_image: str, provider: PixelsProvider):
        self.__image = Image.open(path_to_image)
        self.__pixels = self.__image.load()
        self.__provider = provider

    def pixel_iterator(self) -> Iterator[PixelWrapper]:
        yield from self.__provider.get_iterator(self.__pixels, *self.__image.size)

    def put_pixel(self, pixel: PixelWrapper):
        position, value = pixel.unpack()
        self.__pixels.__setitem__(position, value)

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
