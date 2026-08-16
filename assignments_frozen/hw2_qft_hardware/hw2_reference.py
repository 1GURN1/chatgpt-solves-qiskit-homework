"""
HW2 reference generation and demo grading utilities.

This file is intended to be kept instructor-side. It regenerates the correct
configuration and expected simulator outputs from the student's ID/seed.

Assignment: HW2 - Seeded QFT / inverse-QFT hardware recovery
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any


def stable_seed(student_id: str, assignment_id: str = "HW2") -> int:
    """Return a deterministic integer seed from student_id and assignment_id."""
    key = f"{assignment_id}|{student_id}".encode("utf-8")
    return int(hashlib.sha256(key).hexdigest()[:12], 16)


def _bits_from_seed(seed: int, n: int) -> List[int]:
    """Create a non-trivial, non-palindromic bit pattern in q[0]...q[n-1] order."""
    # Deterministic pseudo-random bits without importing random.
    bits = [(seed >> (3 * i + 1)) & 1 for i in range(n)]
    # Avoid all-zero/all-one and palindromic patterns because they hide bit-order mistakes.
    if sum(bits) in (0, n) or bits == list(reversed(bits)):
        patterns = {
            3: [1, 0, 0],      # displayed reversal visibly differs
            4: [1, 0, 1, 1],
            5: [1, 0, 1, 1, 0],
        }
        bits = patterns.get(n, [1 if i in (0, 2, n-1) else 0 for i in range(n)])
    return bits


def generate_config(student_id: str, assignment_id: str = "HW2") -> Dict[str, Any]:
    """Generate the personalized QFT configuration for one student."""
    seed = stable_seed(student_id, assignment_id)
    n = 3 + (seed % 3)  # 3, 4, or 5 qubits for the autograded simulator core.
    input_bits = _bits_from_seed(seed, n)
    measurement_mode = "direct" if ((seed >> 7) & 1) == 0 else "reversed"
    if measurement_mode == "direct":
        measurement_map = [[i, i] for i in range(n)]
    else:
        measurement_map = [[i, n - 1 - i] for i in range(n)]

    # Hardware is kept small and structured. Students may run the full n if queue/hardware allow.
    hardware_num_qubits = min(n, 3)
    hardware_input_bits = input_bits[:hardware_num_qubits]
    if hardware_input_bits == list(reversed(hardware_input_bits)):
        hardware_input_bits = [1, 0, 0][:hardware_num_qubits]
    hardware_measurement_map = [[i, i] for i in range(hardware_num_qubits)]

    return {
        "assignment_id": assignment_id,
        "student_id": student_id,
        "seed": seed,
        "num_qubits": n,
        "input_bits_q0_to_qn": input_bits,
        "measurement_mode": measurement_mode,
        "measurement_map": measurement_map,
        "hardware_num_qubits": hardware_num_qubits,
        "hardware_input_bits_q0_to_qn": hardware_input_bits,
        "hardware_measurement_map": hardware_measurement_map,
        "shots": 2048,
        "hardware_shots": 4096,
        "qft_convention": "custom QFT followed by custom inverse QFT; both include final swaps",
    }


def expected_display_bitstring_from_bits(bits_q0_to_qn: List[int], measurement_map: List[List[int]]) -> str:
    """Compute the Qiskit displayed count string c[n-1]...c[0]."""
    n = len(bits_q0_to_qn)
    classical_bits = [0] * n
    for q_index, c_index in measurement_map:
        classical_bits[c_index] = bits_q0_to_qn[q_index]
    return "".join(str(classical_bits[i]) for i in reversed(range(n)))


def expected_logical_q_string(bits_q0_to_qn: List[int]) -> str:
    """Return logical qubit string in q[n-1]...q[0] order."""
    return "".join(str(bits_q0_to_qn[i]) for i in reversed(range(len(bits_q0_to_qn))))


def expected_display_bitstring(config: Dict[str, Any]) -> str:
    return expected_display_bitstring_from_bits(config["input_bits_q0_to_qn"], config["measurement_map"])


def expected_hardware_display_bitstring(config: Dict[str, Any]) -> str:
    return expected_display_bitstring_from_bits(config["hardware_input_bits_q0_to_qn"], config["hardware_measurement_map"])


def build_qft_circuit(num_qubits: int, inverse: bool = False):
    """Build a custom QFT or inverse QFT circuit using H, CP, and SWAP gates."""
    from qiskit import QuantumCircuit
    import math

    qc = QuantumCircuit(num_qubits, name="IQFT" if inverse else "QFT")

    if not inverse:
        # QFT: process high to low, then swaps.
        for target in reversed(range(num_qubits)):
            qc.h(target)
            for control in reversed(range(target)):
                angle = math.pi / (2 ** (target - control))
                qc.cp(angle, control, target)
        for i in range(num_qubits // 2):
            qc.swap(i, num_qubits - 1 - i)
    else:
        # Inverse QFT: inverse of the above order.
        for i in range(num_qubits // 2):
            qc.swap(i, num_qubits - 1 - i)
        for target in range(num_qubits):
            for control in range(target):
                angle = -math.pi / (2 ** (target - control))
                qc.cp(angle, control, target)
            qc.h(target)

    return qc


def build_reference_circuit(config: Dict[str, Any], *, hardware_subset: bool = False):
    """Build the reference circuit: prepare basis state, QFT, inverse QFT, measure."""
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

    if hardware_subset:
        n = config["hardware_num_qubits"]
        bits = config["hardware_input_bits_q0_to_qn"]
        measurement_map = config["hardware_measurement_map"]
    else:
        n = config["num_qubits"]
        bits = config["input_bits_q0_to_qn"]
        measurement_map = config["measurement_map"]

    q = QuantumRegister(n, "q")
    c = ClassicalRegister(n, "c")
    qc = QuantumCircuit(q, c)

    for i, bit in enumerate(bits):
        if bit == 1:
            qc.x(q[i])
    qc.barrier(label="prepare")

    qc.compose(build_qft_circuit(n, inverse=False), qubits=list(range(n)), inplace=True)
    qc.barrier(label="after_qft")
    qc.compose(build_qft_circuit(n, inverse=True), qubits=list(range(n)), inplace=True)
    qc.barrier(label="after_iqft")

    for q_index, c_index in measurement_map:
        qc.measure(q[q_index], c[c_index])

    return qc


def simulate_reference_counts(config: Dict[str, Any], shots: int | None = None) -> Dict[str, int]:
    from qiskit import transpile
    from qiskit_aer import AerSimulator

    shots = shots or int(config.get("shots", 2048))
    sim = AerSimulator(seed_simulator=config["seed"] % (2**32 - 1))
    qc = build_reference_circuit(config)
    tqc = transpile(qc, sim, seed_transpiler=config["seed"] % (2**32 - 1), optimization_level=0)
    result = sim.run(tqc, shots=shots).result()
    counts = result.get_counts()
    return {str(k): int(v) for k, v in counts.items()}


def reference_answers(student_id: str, assignment_id: str = "HW2", shots: int | None = None) -> Dict[str, Any]:
    config = generate_config(student_id, assignment_id)
    shots = shots or config["shots"]
    counts = simulate_reference_counts(config, shots=shots)
    expected_display = expected_display_bitstring(config)
    return {
        "assignment_id": assignment_id,
        "student_id": student_id,
        "seed": config["seed"],
        "num_qubits": config["num_qubits"],
        "input_bits_q0_to_qn": config["input_bits_q0_to_qn"],
        "measurement_mode": config["measurement_mode"],
        "measurement_map": config["measurement_map"],
        "expected_logical_qn_to_q0": expected_logical_q_string(config["input_bits_q0_to_qn"]),
        "expected_display_bitstring": expected_display,
        "shots": shots,
        "counts": counts,
        "dominant_bitstring": max(counts, key=counts.get),
    }


def validate_answers(student_answers: Dict[str, Any], student_id: str, assignment_id: str = "HW2") -> Dict[str, Any]:
    """Demo validation function. Real autograders can expand this."""
    ref = reference_answers(student_id, assignment_id, shots=int(student_answers.get("shots", 2048)))
    feedback = []
    score = 0
    max_score = 10

    def check(field, points=1):
        nonlocal score
        if student_answers.get(field) == ref.get(field):
            score += points
            feedback.append(f"PASS: {field}")
        else:
            feedback.append(f"FAIL: {field}. Expected {ref.get(field)!r}, got {student_answers.get(field)!r}")

    check("seed", 1)
    check("num_qubits", 1)
    check("input_bits_q0_to_qn", 1)
    check("measurement_map", 1)
    check("expected_display_bitstring", 2)
    check("dominant_bitstring", 2)

    # Counts: for ideal simulator, expected bitstring should receive all shots.
    expected = ref["expected_display_bitstring"]
    student_counts = {str(k): int(v) for k, v in student_answers.get("counts", {}).items()}
    if student_counts.get(expected, 0) == int(student_answers.get("shots", 0)):
        score += 2
        feedback.append("PASS: simulator counts place all shots on expected bitstring")
    else:
        feedback.append(f"FAIL: simulator counts should put all shots on {expected}")

    return {"score": score, "max_score": max_score, "feedback": feedback, "reference": ref}


if __name__ == "__main__":
    sid = "demo_student"
    print(json.dumps(reference_answers(sid), indent=2))
