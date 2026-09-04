from __future__ import annotations


def build_image() -> bytes:
    # TODO [BOOT-IMAGE-01]: place the real-mode instruction bytes at the beginning and
    # write the legacy boot signature 55 AA at offsets 510..511.
    return bytes(512)


if __name__ == "__main__":
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", default="bootsector.bin")
    args = parser.parse_args()
    Path(args.output).write_bytes(build_image())
