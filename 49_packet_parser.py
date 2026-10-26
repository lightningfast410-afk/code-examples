"""49_packet_parser.py — Parse a binary packet header with struct.

Demonstrates: reading a fixed binary layout (version, type,
length, source, destination, payload) with struct.unpack,
validating the length field against the actual bytes, and
rejecting truncated or inconsistent packets instead of
guessing. Bytes here are synthetic, made up for the demo.
Run: python3 49_packet_parser.py
"""

import struct

HEADER = struct.Struct("!BBHII")  # version, type, length, src, dst


def build_packet(version, ptype, src, dst, payload: bytes):
    length = HEADER.size + len(payload)
    return HEADER.pack(version, ptype, length, src, dst) + payload


def parse_packet(raw: bytes):
    """Return a dict, or raise ValueError on bad input."""
    if len(raw) < HEADER.size:
        raise ValueError("packet shorter than header")
    version, ptype, length, src, dst = HEADER.unpack(raw[:HEADER.size])
    if length != len(raw):
        raise ValueError(f"length field {length} != actual {len(raw)}")
    if version != 1:
        raise ValueError(f"unsupported version {version}")
    return {"version": version, "type": ptype, "src": src, "dst": dst,
            "payload": raw[HEADER.size:]}


def main():
    raw = build_packet(1, 7, 0x0A000001, 0x0A000002, b"hello")
    parsed = parse_packet(raw)
    assert parsed["payload"] == b"hello"
    assert parsed["src"] == 0x0A000001 and parsed["type"] == 7
    rejected = 0
    for bad in (raw[:5], raw[:-1], build_packet(2, 7, 1, 2, b"x")):
        try:
            parse_packet(bad)
        except ValueError:
            rejected += 1
    assert rejected == 3  # truncated, length mismatch, bad version
    print(f"PROOF: parsed payload = {parsed['payload']!r}, "
          f"src = 10.0.0.1, type = 7")
    print(f"PROOF: 3 malformed packets rejected")


if __name__ == "__main__":
    main()
