# LSB Encoder/Decoder

## Description
Naive implementation of steganographic method of image encoding using the least significant bit.

## Usage
Firstly, initialize an image container
```python
try:
    with SteganoImageWrapper(source_image_path) as wrapper:
        ...
except IOError as error:
    print(f"Error occurred: {error}")
```

To put `message` into `wrapper` and save, use next command sequence
```python
wrapper = Encoder(wrapper).encode(message)
wrapper.save(path_to_save)
```
encode method return value can be omitted.

To pull `message` from `wrapper` with length `message_length` use
```python
result = Decoder(wrapper).decode(message_length)
```

## Example
Consider running the following code with `-e` and `-d` flags respectively

```python
import argparse

from lsbencoder.decoder import Decoder
from lsbencoder.encoder import Encoder
from lsbencoder.utils import SteganoImageWrapper


def initialize_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Specify usage mode')
    parser.add_argument("-e", help="Specify -e for encoding", action='store_true')
    parser.add_argument("-d", help="Specify -d for decoding", action='store_true')
    return parser


def encode_handler(wrapper: SteganoImageWrapper):
    message = input("Input message to encode: ")
    path_to_save = input("Input save path (ex. images/result.png): ")
    wrapper = Encoder(wrapper).encode(message)
    wrapper.save(path_to_save)


def decode_handler(wrapper: SteganoImageWrapper) -> str:
    message_length = int(input("Message length (100 is default): "))
    result = Decoder(wrapper).decode(message_length)
    print(result)
    return result


if __name__ == '__main__':
    source_image_path = input("Input path to image: ")
    parser = initialize_parser()
    args = vars(parser.parse_args())
    try:
        with SteganoImageWrapper(source_image_path) as wrapper:
            if args.get("e", False):
                encode_handler(wrapper)
            elif args.get("d", False):
                decode_handler(wrapper)
            else:
                print("You must specify -e for encoding or -d for decoding")
    except IOError as error:
        print(f"Error occurred: {error}")
```

Encoding run:
```
Input path to image: resources/images/test.jpg
Input message to encode: Some message to encode, yo!
Input save path (ex. images/result.png): result.png
```

Decoding run:
```
Input path to image: result.png
Message length (100 is default): 30
Some message to encode, yo!U[R
```

## P.S.
It is not safe to use this implementation, an arbitrary injected container could be recognized.
