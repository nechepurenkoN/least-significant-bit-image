import unittest

from lsbencoder.encoder import Encoder, get_number_bits, encode_bit
from lsbencoder.utils import LSBImageWrapper, PixelWrapper, NaturalOrderPixelsProvider


class BaseEncoderTest(unittest.TestCase):
    def setUp(self):
        self.image_wrapper = LSBImageWrapper("test/resources/images/shrek.jpg", NaturalOrderPixelsProvider())

    def tearDown(self):
        self.image_wrapper.close()

    def test_conversion_from_number_to_bits(self):
        encoder = Encoder(self.image_wrapper)
        conversion_fn = get_number_bits
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0], list(conversion_fn(0)))
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 1], list(conversion_fn(1)))
        self.assertEqual([0, 0, 0, 1, 0, 0, 0, 0], list(conversion_fn(16)))
        self.assertEqual([1, 0, 0, 1, 0, 1, 0, 0], list(conversion_fn(148)))  # 148 = 128 + 16 + 4
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1], list(conversion_fn(255)))
        with self.assertRaises(AttributeError):
            conversion_fn(-1)
        with self.assertRaises(AttributeError):
            conversion_fn(256)

    def test_bit_encoding_into_channel(self):
        encoder = Encoder(self.image_wrapper)
        bit_encoder_fn = encode_bit
        pixel = PixelWrapper((10, 11, 12), (0,0))
        test_channel = 0
        bit_encode = 1
        self.assertEqual(11, bit_encoder_fn(bit_encode, pixel, test_channel).channel_value(
            test_channel))  # apply 1 to 10 -> 11
        self.assertEqual(11, bit_encoder_fn(bit_encode, pixel, test_channel).channel_value(
            test_channel))  # apply 1 to 11 -> 11
        bit_encode = 0
        self.assertEqual(10, bit_encoder_fn(bit_encode, pixel, test_channel).channel_value(
            test_channel))  # apply 0 to 11 -> 10
        self.assertEqual(10, bit_encoder_fn(bit_encode, pixel, test_channel).channel_value(
            test_channel))  # apply 0 to 10 -> 10
