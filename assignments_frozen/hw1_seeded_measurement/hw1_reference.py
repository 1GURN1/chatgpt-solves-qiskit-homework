"""
HW1 hidden reference generation and grading utilities.

Purpose:
This file demonstrates what the syllabus calls "hidden reference generation functions":
functions used by the instructor/autograder to recompute the correct outputs from a
student-specific seed instead of storing one fixed answer. Students may receive a public
configuration generator, but the instructor keeps these validation functions hidden.

HW1 concept:
- A seed produces a personalized number of qubits, initial bit pattern, deterministic
  bit-flip mask, and measurement mapping.
- Students must implement the circuit, run it, export answers.json, and explain bit order.
- The autograder recomputes the expected final logical bits and displayed bitstring.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Any, Tuple


def stable_int_seed(student_id: str, assignment_id: str = "HW1") -> int:
    """Return a deterministic integer seed from student_id and assignment_id."""
    raw = f"{assignment_id}::{student_id}".encode("utf-8")
    return int(hashlib.sha256(raw).hexdigest()[:16], 16)


def _lcg(seed: int):
    """Small deterministic generator independent of Python random version details."""
    state = seed % (2**31 - 1)
    while True:
        state = (1103515245 * state + 12345) % (2**31 - 1)
        yield state


def _non_palindromic_bits(gen, n: int) -> List[int]:
    """Generate a non-palindromic bit list in q[0]..q[n-1] order."""
    while True:
        bits = [next(gen) % 2 for _ in range(n)]
        if any(bits) and bits != list(reversed(bits)):
            return bits


def generate_config(student_id: str, assignment_id: str = "HW1") -> Dict[str, Any]:
    """
    Generate the personalized HW1 configuration.

    Conventions:
    - initial_bits_q0_to_qn lists the starting X-prepared bits in q[0], q[1], ... order.
    - flip_mask_q0_to_qn lists deterministic X flips applied after initial preparation.
    - final_bits_q0_to_qn = initial XOR flip mask.
    - measurement_map contains pairs [qubit_index, classical_bit_index].
    - Qiskit displays count strings as c[n-1]...c[0].
    """
    seed = stable_int_seed(student_id, assignment_id)
    gen = _lcg(seed)

    n = 4 + (next(gen) % 2)  # 4 or 5 qubits
    initial_bits = _non_palindromic_bits(gen, n)

    # Make a sparse but non-empty deterministic flip mask.
    flip_mask = [0] * n
    first_flip = next(gen) % n
    flip_mask[first_flip] = 1
    if next(gen) % 3 == 0:
        second_flip = next(gen) % n
        flip_mask[second_flip] ^= 1

    final_bits = [a ^ b for a, b in zip(initial_bits, flip_mask)]

    # Avoid final display being palindromic where bit-order errors are hidden.
    if final_bits == list(reversed(final_bits)):
        flip_mask[0] ^= 1
        final_bits = [a ^ b for a, b in zip(initial_bits, flip_mask)]

    measurement_mode = "direct" if (next(gen) % 2 == 0) else "reversed"
    if measurement_mode == "direct":
        measurement_map = [[i, i] for i in range(n)]
    else:
        measurement_map = [[i, n - 1 - i] for i in range(n)]

    return {
        "assignment_id": assignment_id,
        "student_id": student_id,
        "seed": seed,
        "num_qubits": n,
        "initial_bits_q0_to_qn": initial_bits,
        "flip_mask_q0_to_qn": flip_mask,
        "final_bits_q0_to_qn": final_bits,
        "measurement_mode": measurement_mode,
        "measurement_map": measurement_map,
        "bit_order_note": "Counts are displayed as c[n-1]...c[0], not q[0]...q[n-1].",
    }


def expected_display_bitstring(config: Dict[str, Any]) -> str:
    """Compute expected displayed counts key c[n-1]...c[0]."""
    n = int(config["num_qubits"])
    final_bits = list(config["final_bits_q0_to_qn"])
    c = [0] * n
    for q_index, c_index in config["measurement_map"]:
        c[c_index] = final_bits[q_index]
    return "".join(str(c[i]) for i in reversed(range(n)))


def expected_logical_q_string(config: Dict[str, Any]) -> str:
    """Return logical final qubit values shown as q[n-1]...q[0]."""
    final_bits = list(config["final_bits_q0_to_qn"])
    return "".join(str(final_bits[i]) for i in reversed(range(len(final_bits))))


def build_reference_circuit(config: Dict[str, Any]):
    """Build the expected circuit. Requires qiskit to be installed."""
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

    n = int(config["num_qubits"])
    q = QuantumRegister(n, "q")
    c = ClassicalRegister(n, "c")
    qc = QuantumCircuit(q, c)

    for i, bit in enumerate(config["initial_bits_q0_to_qn"]):
        if bit:
            qc.x(q[i])
    qc.barrier(label="seeded initial state")

    for i, bit in enumerate(config["flip_mask_q0_to_qn"]):
        if bit:
            qc.x(q[i])
    qc.barrier(label="seeded bit flips")

    for q_index, c_index in config["measurement_map"]:
        qc.measure(q[q_index], c[c_index])

    return qc


def simulate_reference_counts(config: Dict[str, Any], shots: int = 2048) -> Dict[str, int]:
    """Run the reference circuit on AerSimulator and return counts."""
    from qiskit_aer import AerSimulator
    from qiskit import transpile

    qc = build_reference_circuit(config)
    sim = AerSimulator(seed_simulator=int(config["seed"]) % (2**32 - 1))
    tqc = transpile(qc, sim, seed_transpiler=int(config["seed"]) % (2**32 - 1))
    result = sim.run(tqc, shots=shots).result()
    return result.get_counts()


def reference_answers(student_id: str, shots: int = 2048, assignment_id: str = "HW1") -> Dict[str, Any]:
    """Return the expected answers.json content for a given student."""
    config = generate_config(student_id, assignment_id)
    expected = expected_display_bitstring(config)
    return {
        "assignment_id": assignment_id,
        "student_id": student_id,
        "seed": config["seed"],
        "num_qubits": config["num_qubits"],
        "shots": shots,
        "measurement_mode": config["measurement_mode"],
        "measurement_map": config["measurement_map"],
        "initial_bits_q0_to_qn": config["initial_bits_q0_to_qn"],
        "flip_mask_q0_to_qn": config["flip_mask_q0_to_qn"],
        "final_bits_q0_to_qn": config["final_bits_q0_to_qn"],
        "expected_logical_qn_to_q0": expected_logical_q_string(config),
        "expected_display_bitstring": expected,
        "dominant_bitstring": expected,
        "classification": "pass if simulator dominant bitstring equals expected_display_bitstring",
    }


def validate_answers(student_answers: Dict[str, Any], student_id: str, shots: int = 2048) -> Tuple[bool, List[str]]:
    """Simple hidden validation. Returns (passed, feedback_messages)."""
    ref = reference_answers(student_id, shots=shots)
    feedback = []

    required = [
        "assignment_id", "student_id", "seed", "num_qubits", "shots",
        "measurement_map", "initial_bits_q0_to_qn", "flip_mask_q0_to_qn",
        "final_bits_q0_to_qn", "expected_display_bitstring", "dominant_bitstring",
        "counts", "reflection_bit_order", "reflection_bit_flip"
    ]
    for key in required:
        if key not in student_answers:
            feedback.append(f"Missing required key: {key}")

    if feedback:
        return False, feedback

    checks = {
        "assignment_id": ref["assignment_id"],
        "student_id": ref["student_id"],
        "seed": ref["seed"],
        "num_qubits": ref["num_qubits"],
        "shots": ref["shots"],
        "measurement_map": ref["measurement_map"],
        "initial_bits_q0_to_qn": ref["initial_bits_q0_to_qn"],
        "flip_mask_q0_to_qn": ref["flip_mask_q0_to_qn"],
        "final_bits_q0_to_qn": ref["final_bits_q0_to_qn"],
        "expected_display_bitstring": ref["expected_display_bitstring"],
        "dominant_bitstring": ref["dominant_bitstring"],
    }
    for key, expected in checks.items():
        actual = student_answers.get(key)
        if actual != expected:
            feedback.append(f"{key} mismatch. Expected {expected!r}, got {actual!r}.")

    counts = student_answers.get("counts", {})
    if not isinstance(counts, dict):
        feedback.append("counts must be a dictionary.")
    else:
        total = sum(int(v) for v in counts.values()) if counts else 0
        if total != shots:
            feedback.append(f"counts total should equal {shots}, got {total}.")
        expected_key = ref["expected_display_bitstring"]
        if counts.get(expected_key, 0) < int(0.98 * shots):
            feedback.append(f"Expected bitstring {expected_key} should appear in almost all simulator shots.")

    if len(str(student_answers.get("reflection_bit_order", "")).strip()) < 40:
        feedback.append("reflection_bit_order is too short; explain c[n-1]...c[0] ordering.")
    if len(str(student_answers.get("reflection_bit_flip", "")).strip()) < 25:
        feedback.append("reflection_bit_flip is too short; explain initial bits XOR flip mask.")

    return len(feedback) == 0, feedback or ["All checks passed."]


if __name__ == "__main__":
    sid = "demo_student"
    config = generate_config(sid)
    print(json.dumps(config, indent=2))
    print(json.dumps(reference_answers(sid), indent=2))
