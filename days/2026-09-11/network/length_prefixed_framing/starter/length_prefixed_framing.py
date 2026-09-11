import struct
class Framer:
    def __init__(self):
        self.buf = bytearray()
    def encode(self, payload: bytes) -> bytes:
        # TODO [D9-NET-ENCODE]
        raise NotImplementedError
    def feed(self, data: bytes):
        # TODO [D9-NET-FEED]
        raise NotImplementedError
    def decode_one(self):
        # TODO [D9-NET-DECODE]
        raise NotImplementedError
