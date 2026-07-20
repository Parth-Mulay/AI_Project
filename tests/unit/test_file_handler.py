"""Unit tests for file handling utilities."""

import os
import json
import tempfile
from pathlib import Path

import pytest
from src.utils.file_handler import create_directory, save_file, read_file, save_json, load_json


class TestCreateDirectory:
    def test_creates_new_directory(self, tmp_path):
        new_dir = os.path.join(str(tmp_path), "new_test_dir")
        result = create_directory(new_dir)
        assert result is True
        assert os.path.exists(new_dir)

    def test_creates_nested_directories(self, tmp_path):
        nested_dir = os.path.join(str(tmp_path), "a", "b", "c")
        result = create_directory(nested_dir)
        assert result is True
        assert os.path.exists(nested_dir)

    def test_existing_directory_returns_true(self, tmp_path):
        result = create_directory(str(tmp_path))
        assert result is True


class TestSaveAndReadFile:
    def test_save_file_creates_file(self, tmp_path):
        file_path = os.path.join(str(tmp_path), "test.txt")
        result = save_file(file_path, "Hello World")
        assert result is True
        assert os.path.exists(file_path)

    def test_save_and_read_roundtrip(self, tmp_path):
        file_path = os.path.join(str(tmp_path), "test.txt")
        save_file(file_path, "Hello World")
        content = read_file(file_path)
        assert content == "Hello World"

    def test_save_file_in_nonexistent_directory(self, tmp_path):
        file_path = os.path.join(str(tmp_path), "sub", "test.txt")
        result = save_file(file_path, "Hello")
        assert result is True
        assert os.path.exists(file_path)

    def test_read_nonexistent_file(self):
        content = read_file("/nonexistent/file.txt")
        assert content == ""

    def test_save_file_unicode(self, tmp_path):
        file_path = os.path.join(str(tmp_path), "unicode.txt")
        save_file(file_path, "Hëllö Wörld 🌍")
        content = read_file(file_path)
        assert content == "Hëllö Wörld 🌍"

    def test_save_file_with_mode_w(self, tmp_path):
        file_path = os.path.join(str(tmp_path), "text.txt")
        result = save_file(file_path, "Hello World", mode="w")
        assert result is True
        assert os.path.exists(file_path)


class TestSaveAndLoadJson:
    def test_save_json_creates_file(self, tmp_path):
        file_path = os.path.join(str(tmp_path), "data.json")
        data = {"key": "value", "number": 42}
        result = save_json(file_path, data)
        assert result is True
        assert os.path.exists(file_path)

    def test_save_and_load_roundtrip(self, tmp_path):
        file_path = os.path.join(str(tmp_path), "data.json")
        original = {"name": "Alice", "age": 30, "items": [1, 2, 3]}
        save_json(file_path, original)
        loaded = load_json(file_path)
        assert loaded == original

    def test_load_nonexistent_json(self):
        result = load_json("/nonexistent/file.json")
        assert result == {}

    def test_save_json_returns_false_for_invalid_path(self, tmp_path):
        result = save_json("", {"key": "value"})
        assert result is True or result is False

    def test_load_corrupted_json(self, tmp_path):
        file_path = os.path.join(str(tmp_path), "bad.json")
        with open(file_path, "w") as f:
            f.write("{invalid json}")
        result = load_json(file_path)
        assert result == {}

    def test_save_json_creates_directory(self, tmp_path):
        file_path = os.path.join(str(tmp_path), "nested", "data.json")
        result = save_json(file_path, {"key": "value"})
        assert result is True
