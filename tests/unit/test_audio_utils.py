"""Unit tests for AudioUtils."""

import os
import tempfile
import pytest
from src.audio.audio_utils import AudioUtils


class TestAudioUtils:
    def test_supported_format_mp3(self):
        assert AudioUtils.is_supported_format("test.mp3") is True

    def test_supported_format_wav(self):
        assert AudioUtils.is_supported_format("test.wav") is True

    def test_supported_format_m4a(self):
        assert AudioUtils.is_supported_format("test.m4a") is True

    def test_supported_format_flac(self):
        assert AudioUtils.is_supported_format("test.flac") is True

    def test_unsupported_format_txt(self):
        assert AudioUtils.is_supported_format("test.txt") is False

    def test_unsupported_format_pdf(self):
        assert AudioUtils.is_supported_format("test.pdf") is False

    def test_unsupported_format_no_extension(self):
        assert AudioUtils.is_supported_format("test") is False

    def test_get_supported_formats_list(self):
        formats = AudioUtils.get_supported_formats_list()
        assert ".mp3" in formats
        assert ".wav" in formats
        assert ".m4a" in formats
        assert ".flac" in formats
        assert len(formats) >= 4

    def test_get_file_size_mb_existing_file(self):
        with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".txt") as f:
            f.write(b"A" * 1024 * 1024)
            path = f.name
        try:
            size = AudioUtils.get_file_size_mb(path)
            assert size == pytest.approx(1.0, abs=0.1)
        finally:
            os.unlink(path)

    def test_get_file_size_mb_nonexistent_file(self):
        size = AudioUtils.get_file_size_mb("/nonexistent/file.mp3")
        assert size == 0.0

    def test_get_file_size_mb_empty_file(self):
        with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".txt") as f:
            path = f.name
        try:
            size = AudioUtils.get_file_size_mb(path)
            assert size == pytest.approx(0.0, abs=0.01)
        finally:
            os.unlink(path)

    def test_validate_file_exists_true(self):
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as f:
            path = f.name
        try:
            assert AudioUtils.validate_file_exists(path) is True
        finally:
            os.unlink(path)

    def test_validate_file_exists_false(self):
        assert AudioUtils.validate_file_exists("/nonexistent/file.mp3") is False

    def test_get_format_description_mp3(self):
        desc = AudioUtils.get_format_description("test.mp3")
        assert desc == "MPEG Audio"

    def test_get_format_description_wav(self):
        desc = AudioUtils.get_format_description("test.wav")
        assert desc == "Waveform Audio"

    def test_get_format_description_unknown(self):
        desc = AudioUtils.get_format_description("test.xyz")
        assert desc is None

    def test_supported_formats_are_case_insensitive(self):
        assert AudioUtils.is_supported_format("test.MP3") is True
        assert AudioUtils.is_supported_format("test.WAV") is True
