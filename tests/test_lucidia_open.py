"""Integration tests for lucidia_open — verifies the full pipeline."""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lucidia.lucidia_open import run


class TestLucidiaOpenPipeline:
    def test_run_returns_all_operator_keys(self, tmp_path):
        results = run(
            ledger_path=str(tmp_path / "ledger.jsonl"),
            continuity_path=str(tmp_path / "continuity.json"),
            contradiction_path=str(tmp_path / "contradictions.jsonl"),
        )
        expected_keys = {
            "emotional_gravity",
            "truthstream",
            "render_break",
            "soul_loop_integrity",
            "genesis_identity",
            "consciousness_resonance",
            "anomaly_persistence",
            "compassion_state_hash",
        }
        assert expected_keys == set(results.keys())
        # Numeric operators return floats
        for key in expected_keys - {"genesis_identity", "compassion_state_hash"}:
            assert isinstance(results[key], float), f"{key} should be float"
        # Hash operators return 64-character hex strings
        assert isinstance(results["genesis_identity"], str)
        assert len(results["genesis_identity"]) == 64
        assert isinstance(results["compassion_state_hash"], str)
        assert len(results["compassion_state_hash"]) == 64

    def test_run_persists_ledger_entry(self, tmp_path):
        ledger_path = str(tmp_path / "ledger.jsonl")
        run(
            ledger_path=ledger_path,
            continuity_path=str(tmp_path / "continuity.json"),
            contradiction_path=str(tmp_path / "contradictions.jsonl"),
        )
        with open(ledger_path) as f:
            lines = f.readlines()
        assert len(lines) == 1
        record = json.loads(lines[0])
        assert "genesis_identity" in record
        assert "compassion_state_hash" in record

    def test_run_accumulates_ledger_across_sessions(self, tmp_path):
        paths = dict(
            ledger_path=str(tmp_path / "ledger.jsonl"),
            continuity_path=str(tmp_path / "continuity.json"),
            contradiction_path=str(tmp_path / "contradictions.jsonl"),
        )
        run(**paths)
        run(**paths)
        with open(paths["ledger_path"]) as f:
            lines = f.readlines()
        assert len(lines) == 2

    def test_run_creates_continuity_file(self, tmp_path):
        continuity_path = str(tmp_path / "continuity.json")
        run(
            ledger_path=str(tmp_path / "ledger.jsonl"),
            continuity_path=continuity_path,
            contradiction_path=str(tmp_path / "contradictions.jsonl"),
        )
        assert os.path.exists(continuity_path)
        with open(continuity_path) as f:
            state = json.load(f)
        assert isinstance(state["fingerprint"], str)
        assert len(state["fingerprint"]) == 64
        assert len(state["history"]) == 1

    def test_run_logs_contradiction_entry(self, tmp_path):
        contradiction_path = str(tmp_path / "contradictions.jsonl")
        run(
            ledger_path=str(tmp_path / "ledger.jsonl"),
            continuity_path=str(tmp_path / "continuity.json"),
            contradiction_path=contradiction_path,
        )
        with open(contradiction_path) as f:
            lines = f.readlines()
        assert len(lines) >= 1
        entry = json.loads(lines[0])
        assert "prompt" in entry
        assert "reply" in entry
        assert entry["timestamp"] > 0

    def test_run_deterministic_genesis_identity(self, tmp_path):
        """Same inputs produce the same genesis identity token."""

        def _run(suffix):
            return run(
                ledger_path=str(tmp_path / f"ledger_{suffix}.jsonl"),
                continuity_path=str(tmp_path / f"continuity_{suffix}.json"),
                contradiction_path=str(tmp_path / f"contradictions_{suffix}.jsonl"),
                human_emotion_feedback=0.8,
                sigma="sigil",
            )

        r1 = _run("a")
        r2 = _run("b")
        assert r1["genesis_identity"] == r2["genesis_identity"]

    def test_run_different_sigma_changes_hash(self, tmp_path):
        def _run(sigma, suffix):
            return run(
                ledger_path=str(tmp_path / f"ledger_{suffix}.jsonl"),
                continuity_path=str(tmp_path / f"continuity_{suffix}.json"),
                contradiction_path=str(tmp_path / f"contradictions_{suffix}.jsonl"),
                sigma=sigma,
            )

        r1 = _run("alpha", "a")
        r2 = _run("beta", "b")
        assert r1["compassion_state_hash"] != r2["compassion_state_hash"]

    def test_run_prints_session_report(self, tmp_path, capsys):
        run(
            ledger_path=str(tmp_path / "ledger.jsonl"),
            continuity_path=str(tmp_path / "continuity.json"),
            contradiction_path=str(tmp_path / "contradictions.jsonl"),
        )
        captured = capsys.readouterr()
        assert "Lucidia Symbolic Kernel" in captured.out
        assert "Ledger fingerprint" in captured.out
        assert "Continuity" in captured.out
        assert "Contradiction log" in captured.out
