from typing import Iterator, Tuple

from lsbencoder.exceptions import EncoderTooLongMessageException
from lsbencoder.utils import PixelWrapper, LSBImageWrapper


def get_number_bits(number: int) -> Iterator[int]:
    return reversed([bool(number & (1 << shift)) for shift in range(8)])


def encode_bit(bit: int, pixel: PixelWrapper, channel: int) -> PixelWrapper:
    if pixel.channel_value(channel) & 1:
        pixel.change_channel_value(channel, bit - 1)
    else:
        pixel.change_channel_value(channel, bit)
    return pixel


class Encoder:
    def __init__(self, image_wrapper: LSBImageWrapper):
        self.__image = image_wrapper
        self.__iterator = image_wrapper.pixel_iterator()

    def encode(self, message: str):
        message_byte_sequence = list(message.encode("utf-32"))
        channel_index = 0
        pixel = next(self.__iterator)
        for symbol in message_byte_sequence:
            bits = get_number_bits(symbol)
            for bit in bits:
                pixel, channel_index = self.__make_encode_iteration(bit, pixel, channel_index)
        return self.__image

    def __make_encode_iteration(self, bit: int, pixel: PixelWrapper, channel_index: int) -> Tuple[PixelWrapper, int]:
        pixel = encode_bit(bit, pixel, channel_index)
        channel_index = (channel_index + 1) % 3
        if not channel_index:
            try:
                self.__image.put_pixel(pixel)
                pixel = next(self.__iterator)
            except StopIteration:
                raise EncoderTooLongMessageException(
                    "Specified message is too long to encode using provided image")
        return pixel, channel_index
