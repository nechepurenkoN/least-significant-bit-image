from copy import copy
from typing import Iterator, Tuple

from lsbencoder.exceptions import EncoderTooLongMessageException
from lsbencoder.utils import PixelWrapper, SteganoImageWrapper


class Encoder:
    def __init__(self, image_wrapper: SteganoImageWrapper):
        self.__image = copy(image_wrapper)
        self.__pixel_provider = self.__image.next_pixel_getter()

    def encode(self, message: str, charset: str = "utf-8"):
        message_byte_sequence = [x for x in message.encode(charset)]
        channel_index = 0
        pixel = next(self.__pixel_provider)
        for symbol in message_byte_sequence:
            bits = self.__get_number_bits(symbol)
            for bit in bits:
                pixel, channel_index = self.__make_encode_iteration(bit, pixel, channel_index)
        return self.__image

    def __make_encode_iteration(self, bit: int, pixel: PixelWrapper, channel_index: int) -> Tuple[PixelWrapper, int]:
        pixel = self.__encode_bit(bit, pixel, channel_index)
        channel_index = (channel_index + 1) % 3
        if not channel_index:
            try:
                pixel.save()
                pixel = next(self.__pixel_provider)
            except StopIteration:
                raise EncoderTooLongMessageException(
                    "Specified message is too long to encode using provided image")
        return pixel, channel_index

    def __encode_bit(self, bit: int, pixel: PixelWrapper, channel: int) -> PixelWrapper:
        if pixel.channel_value(channel) & 1:
            pixel.change_channel_value(channel, bit - 1)
        else:
            pixel.change_channel_value(channel, bit)
        return pixel

    def __get_number_bits(self, number: int) -> Iterator[int]:
        return reversed([bool(number & (1 << shift)) for shift in range(8)])
