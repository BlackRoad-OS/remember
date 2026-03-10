"""Tests for the Lucidia symbolic kernel."""

import os
import sys
import json
import tempfile
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from symbolic_kernel import (
    Tri, TruthFragment, HeldContradiction, Breath, RealityEmotion,
    InfinityMemory, MemoryLedger, Continuity,
    psi_prime, emotional_gravity, truthstream, render_break,
    soul_loop_integrity, genesis_identity, consciousness_resonance,
    anomaly_persistence, compassion_state_encrypt,
)


class TestPsiPrime:
    def test_identical_values(self):
        hc = psi_prime(1.0, 1.0)
        assert hc.compassion == 1.0
        assert hc.x == 1.0
        assert hc.x_bar == 1.0

    def test_opposite_values(self):
        hc = psi_prime(1.0, -1.0)
        assert hc.compassion == 0.0
        assert hc.render == 0.0

    def test_no_mirror(self):
        hc = psi_prime(5.0, None)
        assert hc.x_bar == -5.0

    def test_zero_values(self):
        hc = psi_prime(0.0, 0.0)
        assert hc.compassion == 1.0
        assert hc.render == 0.0

    def test_returns_held_contradiction(self):
        hc = psi_prime(0.5, 0.3)
        assert isinstance(hc, HeldContradiction)
        assert "tension" in hc.detail
        assert "mag" in hc.detail


class TestBreath:
    def test_integral(self):
        b = Breath([1.0, 2.0, 3.0])
        assert b.integral() == 6.0

    def test_grad(self):
        b = Breath([1.0, 3.0, 2.0])
        assert b.grad() == [2.0, -1.0]

    def test_empty_timeline(self):
        b = Breath([])
        assert b.integral() == 0.0
        assert b.grad() == []

    def test_single_value(self):
        b = Breath([5.0])
        assert b.integral() == 5.0
        assert b.grad() == []


class TestRealityEmotion:
    def test_correlated_streams(self):
        re = RealityEmotion(
            reality=[1.0, 2.0, 3.0, 4.0, 5.0],
            emotion=[1.0, 2.0, 3.0, 4.0, 5.0],
        )
        slope = re.dReality_over_dEmotion()
        assert abs(slope - 1.0) < 0.01

    def test_mismatched_lengths(self):
        re = RealityEmotion(reality=[1.0], emotion=[1.0, 2.0])
        assert re.dReality_over_dEmotion() == 0.0

    def test_single_value(self):
        re = RealityEmotion(reality=[1.0], emotion=[1.0])
        assert re.dReality_over_dEmotion() == 0.0


class TestInfinityMemory:
    def test_accumulate(self):
        m = InfinityMemory()
        assert m.accumulate(1.0) == 1.0
        assert m.accumulate(2.0) == 3.0
        assert m.total == 3.0

    def test_starts_at_zero(self):
        m = InfinityMemory()
        assert m.total == 0.0


class TestMemoryLedger:
    def test_append_and_fingerprint(self, tmp_path):
        ledger = MemoryLedger(str(tmp_path / "test.jsonl"))
        h1 = ledger.append({"key": "value1"})
        h2 = ledger.append({"key": "value2"})
        assert h1 != h2
        assert ledger.fingerprint == h2
        assert len(h2) == 64

    def test_hash_chain_integrity(self, tmp_path):
        ledger = MemoryLedger(str(tmp_path / "chain.jsonl"))
        ledger.append({"a": 1})
        fp1 = ledger.fingerprint
        ledger.append({"b": 2})
        fp2 = ledger.fingerprint
        # Chain should be deterministic
        ledger2 = MemoryLedger(str(tmp_path / "chain2.jsonl"))
        ledger2.append({"a": 1})
        assert ledger2.fingerprint == fp1

    def test_file_written(self, tmp_path):
        path = str(tmp_path / "out.jsonl")
        ledger = MemoryLedger(path)
        ledger.append({"test": True})
        with open(path) as f:
            lines = f.readlines()
        assert len(lines) == 1
        assert json.loads(lines[0])["test"] is True


class TestContinuity:
    def test_initial_state(self, tmp_path):
        c = Continuity(str(tmp_path / "cont.json"))
        assert c.state["fingerprint"] is None
        assert c.state["history"] == []

    def test_update_fingerprint(self, tmp_path):
        c = Continuity(str(tmp_path / "cont.json"))
        fp, prev = c.update_fingerprint("hello", "world")
        assert len(fp) == 64
        assert prev is None
        fp2, prev2 = c.update_fingerprint("different")
        assert fp2 != fp
        assert prev2 == fp

    def test_same_input_no_change(self, tmp_path):
        c = Continuity(str(tmp_path / "cont.json"))
        fp1, _ = c.update_fingerprint("same")
        fp2, prev = c.update_fingerprint("same")
        assert fp1 == fp2
        assert len(c.state["history"]) == 1  # Only first update recorded

    def test_amnesia_alert(self, tmp_path):
        c = Continuity(str(tmp_path / "cont.json"))
        assert not c.amnesia_alert()
        c.update_fingerprint("trigger")
        assert c.amnesia_alert()  # Just happened, within 60s


class TestKernelFunctions:
    @pytest.fixture
    def breath(self):
        return Breath([0.2, 0.3, 0.1, 0.0, -0.1])

    @pytest.fixture
    def fragments(self):
        return [
            TruthFragment("x1", 0.9, -0.8, emotion=0.7),
            TruthFragment("x2", -0.6, 0.6, emotion=-0.3),
            TruthFragment("x3", 0.4, None, emotion=0.2),
        ]

    def test_emotional_gravity(self, breath):
        result = emotional_gravity(breath, [0.5, 0.5, 0.5, 0.5])
        assert isinstance(result, float)

    def test_truthstream(self, fragments, breath):
        result = truthstream(fragments, breath)
        assert isinstance(result, float)

    def test_render_break(self, fragments):
        result = render_break(fragments, elapsed_steps=10)
        assert isinstance(result, float)

    def test_render_break_zero_steps(self, fragments):
        result = render_break(fragments, elapsed_steps=0)
        assert isinstance(result, float)

    def test_soul_loop_integrity(self, breath):
        result = soul_loop_integrity(0.5, breath, 0.2)
        assert isinstance(result, float)

    def test_genesis_identity_deterministic(self, breath):
        m1 = InfinityMemory()
        m2 = InfinityMemory()
        id1 = genesis_identity(breath, 0.8, m1)
        id2 = genesis_identity(Breath(breath.timeline.copy()), 0.8, m2)
        assert id1 == id2
        assert len(id1) == 64

    def test_consciousness_resonance(self, breath):
        result = consciousness_resonance(0.7, breath, [0.1] * len(breath.timeline))
        assert isinstance(result, float)

    def test_anomaly_persistence(self, fragments):
        echoes = {"x1": [0.2, 0.25], "x2": [0.1, 0.05]}
        result = anomaly_persistence(fragments, echoes)
        assert isinstance(result, float)

    def test_anomaly_persistence_no_series(self, fragments):
        result = anomaly_persistence(fragments, {})
        assert result == 0.0

    def test_compassion_state_encrypt(self, fragments, breath):
        h1 = compassion_state_encrypt(fragments, breath, "sigil")
        h2 = compassion_state_encrypt(fragments, breath, "sigil")
        assert h1 == h2
        assert len(h1) == 64

    def test_compassion_different_sigma(self, fragments, breath):
        h1 = compassion_state_encrypt(fragments, breath, "a")
        h2 = compassion_state_encrypt(fragments, breath, "b")
        assert h1 != h2

    def test_compassion_empty_fragments(self, breath):
        result = compassion_state_encrypt([], breath, "test")
        assert len(result) == 64


class TestTri:
    def test_values(self):
        assert Tri.NEG == -1
        assert Tri.ZERO == 0
        assert Tri.POS == 1
