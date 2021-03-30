from lsbencoder.decoder import Decoder
from lsbencoder.encoder import Encoder
from lsbencoder.utils import SteganoImageWrapper

if __name__ == '__main__':
    mode = input("Mode:")
    if mode == "e":
        wrapper = SteganoImageWrapper("../resources/images/test.jpg")
        wrapper = Encoder(wrapper).encode("Hello, world!")
        wrapper.save("../resources/images/result.png")
    else:
        wrapper = SteganoImageWrapper("../resources/images/result.png")
        print(Decoder(wrapper).decode())
#[72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]