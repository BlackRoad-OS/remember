"""Tests for the contradiction log."""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lucidia.contradiction_log import ContradictionLog, ContradictionEntry


class TestContradictionLog:
    def test_append_and_read(self, tmp_path):
        log = ContradictionLog(str(tmp_path / "test.jsonl"))
        log.append("prompt1", "reply1")
        entries = log.read_all()
        assert len(entries) == 1
        assert entries[0].prompt == "prompt1"
        assert entries[0].reply == "reply1"
        assert entries[0].timestamp > 0

    def test_multiple_entries(self, tmp_path):
        log = ContradictionLog(str(tmp_path / "test.jsonl"))
        log.append("p1", "r1")
        log.append("p2", "r2")
        log.append("p3", "r3")
        entries = log.read_all()
        assert len(entries) == 3
        assert entries[2].prompt == "p3"

    def test_read_nonexistent_file(self, tmp_path):
        log = ContradictionLog(str(tmp_path / "missing.jsonl"))
        entries = log.read_all()
        assert entries == []

    def test_timestamps_increase(self, tmp_path):
        log = ContradictionLog(str(tmp_path / "test.jsonl"))
        log.append("first", "a")
        log.append("second", "b")
        entries = log.read_all()
        assert entries[1].timestamp >= entries[0].timestamp

    def test_entry_dataclass(self):
        entry = ContradictionEntry(timestamp=1.0, prompt="p", reply="r")
        assert entry.timestamp == 1.0
        assert entry.prompt == "p"
        assert entry.reply == "r"
