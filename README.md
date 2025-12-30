# serum-preset-packager

This CLI tool allows to unpack and pack `SerumPreset` files (and others) used by [Serum 2](https://xferrecords.com/products/serum-2).

The file format was not open so far and it took a bit of reverse engineering to understand the file format.

> [!TIP]
> Looking for a `.SerumPreset` editor and organizer? [See preset.tools](https://preset.tools)<br/>
> It's based on this project and offers an easy to use web-based editor for preset metadata.

## Usage

1. Clone the repo
2. Install pip dependencies `pip install -r requirements.txt`

### Unpack

Unpacking will decompress and dump the data in the preset file into a JSON file.

> [!NOTE]  
> The tool also supports some other file extensions used by Serum 2 like `.XferArpBank`. The legacy `.fxp` is [NOT supported](https://github.com/KennethWussmann/serum-preset-packager/issues/1).
 
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

### Edit

The edit command provides a convenient way to modify a preset file in one step. It unpacks the preset to a temporary JSON file, opens it in your editor, and automatically packs it back when you save and exit.

```shell
python cli.py edit MyPreset.SerumPreset
```

This will:
1. Unpack the preset to a temporary JSON file
2. Open the file in your `$EDITOR` (defaults to `vi` if not set)
3. Wait for you to save and close the editor
4. Pack the modified JSON back to the original preset file
5. Clean up the temporary file automatically

## File Format

Kudos to [@0xdevalias](https://github.com/0xdevalias) for [his Gist](https://gist.github.com/0xdevalias/5a06349b376d01b2a76ad27a86b08c1b) on the reverse engineering of the preset file format. That sparked my interest to look further into it.

The file is structured like:
1. Header + metadata JSON (`b"XferJson\x00" + uint64_le(len(json)) + json-bytes`)
2. Zstandard compressed CBOR payload (`uint32_le(len(cbor)) + uint32_le(2) + zstd‑frame(cbor-bytes)`)

Check the implementation for details. Yet unclear is the CBOR data itself. We can unpack and modify what is there, but what are valid properties is unknown. You can probably enumerate by unpacking all preset files you can find and eventually come across all possible values.

## Related Projects

- [preset.tools](https://preset.tools) - a web-based `.SerumPreset` metadata editor and collection organizer.
- [node-serum2-preset-packager](https://github.com/CharlesBT/node-serum2-preset-packager) - based on this research, CLI and TypeScript, Node API.
