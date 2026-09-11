import struct
class Framer:
    def __init__(self):
        self.buf = bytearray()
    def encode(self, payload: bytes) -> bytes:
        # PEDAGOGY-SOLUTION: D9-NET-ENCODE
        return struct.pack("<I", len(payload)) + payload
    def feed(self, data: bytes):
        # PEDAGOGY-SOLUTION: D9-NET-FEED
        self.buf.extend(data)
    def decode_one(self):
        # PEDAGOGY-SOLUTION: D9-NET-DECODE
        if len(self.buf) < 4:
            return None
        (n,) = struct.unpack_from("<I", self.buf, 0)
        if len(self.buf) < 4 + n:
            return None
        payload = bytes(self.buf[4:4+n])
        del self.buf[:4+n]
        return payload
