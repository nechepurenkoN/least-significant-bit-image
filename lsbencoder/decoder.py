from copy import copy
from typing import Iterator

from lsbencoder.utils import SteganoImageWrapper


class Decoder:
    def __init__(self, image_wrapper: SteganoImageWrapper):
        self.__image = copy(image_wrapper)
        self.__pixel_provider = self.__image.next_pixel_getter()

    def decode(self) -> str:
        bits_generator = self.__bits_getter()
        char_codes = []
        try:
            while True:
                code_accumulator = 0
                for shift in range(7, -1, -1):
                    bit = next(bits_generator)
                    code_accumulator = code_accumulator + (bit << shift)
                char_codes.append(code_accumulator)
        except StopIteration:
            pass
        return "".join(map(chr, char_codes[:20]))

    def __bits_getter(self) -> Iterator[int]:
        for pixel in self.__pixel_provider:
            for channel in range(3):
                yield pixel.channel_value(channel) & 1
