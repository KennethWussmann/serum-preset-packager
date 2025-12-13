import pytest
import pathlib
import tempfile
import json
from cli import unpack, pack


@pytest.fixture
def test_preset():
    """Path to the test SerumPreset file."""
    return pathlib.Path(__file__).parent.parent / "test" / "test.SerumPreset"


@pytest.fixture
def temp_json():
    """Create a temporary JSON file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        tmp_path = pathlib.Path(tmp.name)
    yield tmp_path
    tmp_path.unlink(missing_ok=True)


@pytest.fixture
def temp_preset():
    """Create a temporary preset file."""
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".SerumPreset", delete=False) as tmp:
        tmp_path = pathlib.Path(tmp.name)
    yield tmp_path
    tmp_path.unlink(missing_ok=True)


def test_unpack_preset_snapshot(test_preset, temp_json, snapshot):
    """Test unpacking a SerumPreset file and verify output with snapshot."""
    unpack(test_preset, temp_json)

    # Load the unpacked JSON
    with open(temp_json, "r") as f:
        unpacked_data = json.load(f)

    # Snapshot the unpacked data
    assert unpacked_data == snapshot


def test_pack_preset(test_preset, temp_json, temp_preset):
    """Test packing a JSON file back to SerumPreset format."""
    # First unpack the original preset
    unpack(test_preset, temp_json)

    # Then pack it back
    pack(temp_json, temp_preset)

    # Verify the packed file exists and has content
    assert temp_preset.exists()
    assert temp_preset.stat().st_size > 0


def test_round_trip_conversion(test_preset, temp_json, temp_preset, snapshot):
    """Test that unpacking and repacking produces consistent results."""
    # Unpack original preset
    unpack(test_preset, temp_json)

    # Load the JSON
    with open(temp_json, "r") as f:
        original_json = json.load(f)

    # Pack it back to a new preset file
    pack(temp_json, temp_preset)

    # Unpack the repacked preset to a new JSON file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        repacked_json_path = pathlib.Path(tmp.name)

    try:
        unpack(temp_preset, repacked_json_path)

        # Load the repacked JSON
        with open(repacked_json_path, "r") as f:
            repacked_json = json.load(f)

        # The round-trip should produce identical JSON
        assert original_json == repacked_json

        # Also snapshot the round-trip result
        assert repacked_json == snapshot
    finally:
        repacked_json_path.unlink(missing_ok=True)


def test_metadata_preserved(test_preset, temp_json, snapshot):
    """Test that metadata is correctly preserved during unpacking."""
    unpack(test_preset, temp_json)

    with open(temp_json, "r") as f:
        data = json.load(f)

    # Verify metadata structure exists
    assert "metadata" in data
    assert "data" in data

    # Snapshot the metadata specifically
    assert data["metadata"] == snapshot


def test_preset_file_structure(test_preset):
    """Test that the preset file has the expected binary structure."""
    content = test_preset.read_bytes()

    # Check magic header
    assert content.startswith(b"XferJson\x00")

    # Verify file is not empty
    assert len(content) > 0
