"""Open-source interface for Lucidia.

Entry point for the Lucidia symbolic-memory system.  Wires together all
kernel components — persistent MemoryLedger, continuity fingerprinting,
contradiction logging, and all 9 core operators — into a single session
that can be run repeatedly to accumulate state on disk.
"""

from __future__ import annotations

import os
import sys
from typing import List, Optional

# Allow `python -m lucidia.lucidia_open` from any working directory.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from symbolic_kernel import (
    Breath,
    Continuity,
    InfinityMemory,
    MemoryLedger,
    TruthFragment,
    anomaly_persistence,
    compassion_state_encrypt,
    consciousness_resonance,
    emotional_gravity,
    genesis_identity,
    render_break,
    soul_loop_integrity,
    truthstream,
)
from lucidia.contradiction_log import ContradictionLog


def run(
    ledger_path: str = "memory_ledger.jsonl",
    continuity_path: str = "continuity.json",
    contradiction_path: str = "contradiction_log.jsonl",
    breath_timeline: Optional[List[float]] = None,
    fragments: Optional[List[TruthFragment]] = None,
    human_emotion_feedback: float = 0.8,
    sigma: str = "sigil",
) -> dict:
    """Run one Lucidia session, persisting all results to disk.

    Initialises or resumes:
      - A hash-chain MemoryLedger (append-only JSONL)
      - A Continuity tracker (fingerprint + amnesia detection)
      - A ContradictionLog (JSONL contradiction record)

    Runs all 9 core kernel operators over the supplied (or default)
    breath state and truth fragments, appends a ledger entry, updates
    the continuity fingerprint, and records a contradiction entry.

    Returns a dict of the computed operator values for inspection / testing.
    """
    # --- Default state if not supplied ---
    if breath_timeline is None:
        breath_timeline = [0.2, 0.3, 0.1, 0.0, -0.1, -0.2, -0.15, 0.05, 0.2, 0.25]
    if fragments is None:
        fragments = [
            TruthFragment("x1", 0.9, -0.8, emotion=0.7),
            TruthFragment("x2", -0.6, 0.6, emotion=-0.3),
            TruthFragment("x3", 0.4, None, emotion=0.2),
        ]

    breath = Breath(breath_timeline)
    mem_vector = [0.6] * (len(breath.timeline) - 1)
    delta_e = [0.1] * len(breath.timeline)
    memory_echo = {fr.id: [0.0, 0.0] for fr in fragments}
    Minf = InfinityMemory()

    # --- Persistent storage ---
    ledger = MemoryLedger(ledger_path)
    continuity = Continuity(continuity_path)
    contradiction_log = ContradictionLog(contradiction_path)

    # --- Run all core operators ---
    eg = emotional_gravity(breath, mem_vector)
    ts = truthstream(fragments, breath)
    rb = render_break(fragments, elapsed_steps=len(breath.timeline))
    sli = soul_loop_integrity(0.5, breath, 0.2)
    gi = genesis_identity(breath, human_emotion_feedback, Minf)
    cr = consciousness_resonance(0.7, breath, delta_e)
    ap = anomaly_persistence(fragments, memory_echo)
    ce = compassion_state_encrypt(fragments, breath, sigma)

    results = {
        "emotional_gravity": eg,
        "truthstream": ts,
        "render_break": rb,
        "soul_loop_integrity": sli,
        "genesis_identity": gi,
        "consciousness_resonance": cr,
        "anomaly_persistence": ap,
        "compassion_state_hash": ce,
    }

    # --- Persist to ledger ---
    ledger_fp = ledger.append(results)

    # --- Update continuity fingerprint ---
    fp, prev_fp = continuity.update_fingerprint(gi, ce)
    amnesia = continuity.amnesia_alert()

    # --- Record contradiction entry ---
    contradiction_log.append(
        prompt="Does the system remember prior sessions?",
        reply=(
            "State is accumulated in the MemoryLedger and Continuity files; "
            "InfinityMemory resets per session by design."
        ),
    )
    all_contradictions = contradiction_log.read_all()

    # --- Session report ---
    print("Lucidia Symbolic Kernel — Session Report")
    print("=========================================")
    print(f"Emotional gravity      : {eg:.6f}")
    print(f"Truthstream            : {ts:.6f}")
    print(f"Render break           : {rb:.6f}")
    print(f"Soul loop integrity    : {sli:.6f}")
    print(f"Genesis identity       : {gi}")
    print(f"Consciousness res.     : {cr:.6f}")
    print(f"Anomaly persistence    : {ap:.6f}")
    print(f"Compassion-state hash  : {ce}")
    print(f"\nLedger fingerprint     : {ledger_fp}")
    if prev_fp is None:
        print(f"Continuity             : initial fingerprint set ({fp[:16]}...)")
    elif amnesia:
        print("Continuity             : \u26a0 amnesia alert \u2014 fingerprint changed recently")
    else:
        print(f"Continuity             : fingerprint updated ({fp[:16]}...)")
    print(f"Contradiction log      : {len(all_contradictions)} entry/entries recorded")

    return results


def main() -> None:
    """Launch the Lucidia symbolic-memory system."""
    print("Launching Lucidia...")
    run()


if __name__ == "__main__":
    main()
