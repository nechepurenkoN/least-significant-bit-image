import argparse

from lsbencoder.decoder import Decoder
from lsbencoder.encoder import Encoder
from lsbencoder.utils import LSBImageWrapper, NaturalOrderPixelsProvider


def initialize_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Specify usage mode')
    parser.add_argument("-e", help="Specify -e for encoding", action='store_true')
    parser.add_argument("-d", help="Specify -d for decoding", action='store_true')
    return parser


def encode_handler(wrapper: LSBImageWrapper):
    message = input("Input message to encode: ")
    path_to_save = input("Input save path (ex. images/result.png): ")
    wrapper = Encoder(wrapper).encode(message)
    wrapper.save(path_to_save)


def decode_handler(wrapper: LSBImageWrapper) -> str:
    result = Decoder(wrapper).decode()
    print(result)
    return result


if __name__ == '__main__':
    source_image_path = input("Input path to image: ")
    parser = initialize_parser()
    args = vars(parser.parse_args())
    try:
        with LSBImageWrapper(source_image_path, NaturalOrderPixelsProvider()) as wrapper:
            if args.get("e", False):
                encode_handler(wrapper)
            elif args.get("d", False):
                decode_handler(wrapper)
            else:
                print("You must specify -e for encoding or -d for decoding")
    except IOError as error:
        print(f"Error occurred: {error}")
