from typing import Iterator

from lsbencoder.utils import LSBImageWrapper

shift_range = range(7, -1, -1)


class Decoder:
    def __init__(self, image_wrapper: LSBImageWrapper):
        self.__image = image_wrapper
        self.__iterator = image_wrapper.pixel_iterator()

    def decode(self) -> str:
        bits_generator = self.__bits_getter()
        char_codes = []
        try:
            while True:
                code_accumulator = 0
                for shift in shift_range:
                    bit = next(bits_generator)
                    code_accumulator = code_accumulator + (bit << shift)
                char_codes.append(code_accumulator)
        except StopIteration:
            pass
        return bytes(char_codes).decode("utf-32", "ignore")

    def __bits_getter(self) -> Iterator[int]:
        for pixel in self.__iterator:
            for channel in range(3):
                yield pixel.channel_value(channel) & 1
