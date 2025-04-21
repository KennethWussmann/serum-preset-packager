#!/usr/bin/env python3
import sys, json, struct, pathlib, cbor2, zstandard as zstd

MAGIC = b"XferJson\x00"

def unpack(src: pathlib.Path, dst: pathlib.Path):
    buf = src.read_bytes()
    off = len(MAGIC)
    jlen, _ = struct.unpack_from("<II", buf, off); off += 8
    meta = json.loads(buf[off:off + jlen]); off += jlen
    clen, _ = struct.unpack_from("<II", buf, off); off += 8
    cbor = zstd.ZstdDecompressor().decompress(buf[off:])
    assert len(cbor) == clen
    dst.write_text(json.dumps({"metadata": meta, "data": cbor2.loads(cbor)}, indent=2))

def pack(src: pathlib.Path, dst: pathlib.Path):
    obj = json.loads(src.read_text())
    m = json.dumps(obj["metadata"], separators=(",", ":")).encode()
    c = cbor2.dumps(obj["data"])
    z = zstd.ZstdCompressor(level=3).compress(c)
    out = bytearray()
    out += MAGIC
    out += struct.pack("<II", len(m), 0)
    out += m
    out += struct.pack("<II", len(c), 2)
    out += z
    dst.write_bytes(out)

if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] not in {"unpack", "pack"}:
        print("usage: cli.py unpack <file.SerumPreset> <out.json>\n"
              "       cli.py pack   <in.json>         <out.SerumPreset>")
        sys.exit(1)
    (unpack if sys.argv[1] == "unpack" else pack)(pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]))
