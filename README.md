# serum-preset-packager

This CLI tool allows to unpack and pack `SerumPreset` files (and others) used by [Serum 2](https://xferrecords.com/products/serum-2).

The file format was not open so far and it took a bit of reverse engineering to understand the file format.

## Usage

1. Clone the repo
2. Install pip dependencies `pip install -r requirements.txt`

### Unpack

Unpacking will decompress and dump the data in the preset file into a JSON file.

> [!NOTE]  
> The tool also supports some other file extensions used by Serum 2 like `.XferArpBank`. The legacy `.fxp` is NOT supported.
 
```shell
python cli.py unpack MyPreset.SerumPreset MyPreset.json
```

You can now look at and edit the `MyPreset.json`. Once you are done, you can pack the JSON back.

### Pack

Packing means converting the JSON back into a valid Serum 2 preset file.

```shell
python cli.py pack MyPreset.json MyPreset.SerumPreset
```

This will produce a valid `SerumPreset` that you can load into Serum 2.

## File Format

Kudos to [@0xdevalias](https://github.com/0xdevalias) for [his Gist](https://gist.github.com/0xdevalias/5a06349b376d01b2a76ad27a86b08c1b) on the reverse engineering of the preset file format. That sparked my interest to look further into it.

The file is structured like:
1. Header + metadata JSON (`b"XferJson\x00" + uint64_le(len(json)) + json-bytes`)
2. Zstandard compressed CBOR payload (`uint32_le(len(cbor)) + uint32_le(2) + zstd‑frame(cbor-bytes)`)

Check the implementation for details. Yet unclear is the CBOR data itself. We can unpack and modify what is there, but what are valid properties is unknown. You can probably enumerate by unpacking all preset files you can find and eventually come across all possible values.
