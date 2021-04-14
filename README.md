# LSB Encoder/Decoder

## Description
Naive implementation of a steganographic method of an image encoding using the least significant bit.

## Usage
Firstly, initialize an image container
```python
try:
    with LSBImageWrapper(source_image_path, NaturalOrderPixelsProvider()) as wrapper:
        ...
except IOError as error:
    print(f"Error occurred: {error}")
```

The second argument of the container is an implementation of 
```python
class PixelsProvider:
    @abc.abstractmethod
    def get_iterator(self, pixels: PyAccess, width: int, height: int) -> Iterator[PixelWrapper]:
        raise NotImplementedError
```
which specifies the order of pixels.

It might be `NaturalOrderPixelsProvider` as in the example.
```python
class NaturalOrderPixelsProvider(PixelsProvider, ABC):
    def get_iterator(self, pixels: PyAccess, width: int, height: int) -> Iterator[PixelWrapper]:
        for x in range(height):
            for y in range(width):
                yield PixelWrapper(pixels[y, x], (y, x))
```

To put `message` into `wrapper` and save, use next command sequence
```python
wrapper = Encoder(wrapper).encode(message)
wrapper.save(path_to_save)
```
encode method return value can be omitted.

To pull `message` from `wrapper` with length `message_length` use
```python
result = Decoder(wrapper).decode()
```

## Example
Consider running the following code with `-e` and `-d` flags respectively

```python
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
```

Encoding run:
```
Input path to image: resources/images/test.jpg
Input message to encode: Hello, world! Здесь может быть любой текст, даже такой　孫子兵法 или такой 😍.
Input save path (ex. images/result.png): resources/images/result.png
```

Decoding run:
```
Input path to image: resources/images/result.png
Hello, world! Здесь может быть любой текст, даже такой　孫子兵法 или такой 😍沛
```

## P.S.
It is not safe to use this implementation, an arbitrary injected container could be recognized.
