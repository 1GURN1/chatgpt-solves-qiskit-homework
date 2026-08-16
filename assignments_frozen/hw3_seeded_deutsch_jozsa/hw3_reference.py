"""
HW3 Seeded Deutsch-Jozsa reference functions.

Instructor/autograder-side utilities for generating deterministic student-specific
Deutsch-Jozsa assignments, reference outputs, and grading feedback.

Important conventions:
- mask_q0_to_qn is listed in q[0], q[1], ..., q[n-1] order.
- Qiskit count strings are displayed as c[n-1]...c[0].
- Only input qubits are measured. The output/ancilla qubit is not measured for grading.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


def stable_seed(student_id: str, assignment_id: str = "HW3") -> int:
    key = f"{assignment_id}|{student_id}".encode("utf-8")
    return int(hashlib.sha256(key).hexdigest()[:12], 16)


def _bits_from_seed(seed: int, n: int, offset: int = 0) -> List[int]:
    return [(seed >> (offset + i)) & 1 for i in range(n)]


def _is_palindrome(bits: List[int]) -> bool:
    return bits == list(reversed(bits))


def _make_nonzero_nonpal_mask(seed: int, n: int) -> List[int]:
    # Try several seed shifts until the mask is nonzero and not a palindrome.
    for shift in range(0, 40, 3):
        mask = _bits_from_seed(seed, n, shift)
        if any(mask) and not _is_palindrome(mask):
            return mask
    # Deterministic fallback that works for n >= 3.
    mask = [0] * n
    mask[0] = 1
    mask[-2] = 1
    if _is_palindrome(mask):
        mask[1] ^= 1
    return mask


def generate_config(student_id: str, assignment_id: str = "HW3") -> Dict[str, Any]:
    """Generate a deterministic HW3 task from a student ID.

    Students receive this config. It intentionally includes the oracle mask and
    output_offset but does not include the expected measured bitstring.
    """
    seed = stable_seed(student_id, assignment_id)
    n = 3 + (seed % 3)  # 3, 4, or 5 input qubits for simulator/autograded core.

    # About 1/3 of students receive a constant oracle. The rest receive balanced.
    make_constant = ((seed >> 5) % 3 == 0)
    if make_constant:
        mask = [0] * n
    else:
        mask = _make_nonzero_nonpal_mask(seed >> 8, n)

    output_offset = (seed >> 17) & 1  # f(x) = mask dot x XOR output_offset

    # Measurement mode for the input register only.
    measurement_mode = "reversed" if ((seed >> 19) & 1) else "direct"
    if measurement_mode == "direct":
        measurement_map = [[i, i] for i in range(n)]
    else:
        measurement_map = [[i, n - 1 - i] for i in range(n)]

    # Small fixed-size hardware extension. Use a separate generated mask but the same logic.
    hw_n = 3
    hw_make_constant = ((seed >> 23) % 4 == 0)
    if hw_make_constant:
        hw_mask = [0] * hw_n
    else:
        hw_mask = _make_nonzero_nonpal_mask(seed >> 25, hw_n)
    hw_output_offset = (seed >> 31) & 1
    hw_measurement_mode = "reversed" if ((seed >> 32) & 1) else "direct"
    if hw_measurement_mode == "direct":
        hw_measurement_map = [[i, i] for i in range(hw_n)]
    else:
        hw_measurement_map = [[i, hw_n - 1 - i] for i in range(hw_n)]

    return {
        "assignment_id": assignment_id,
        "student_id": student_id,
        "seed": seed,
        "num_input_qubits": n,
        "mask_q0_to_qn": mask,
        "output_offset": output_offset,
        "measurement_mode": measurement_mode,
        "measurement_map": measurement_map,
        "hardware_num_input_qubits": hw_n,
        "hardware_mask_q0_to_qn": hw_mask,
        "hardware_output_offset": hw_output_offset,
        "hardware_measurement_mode": hw_measurement_mode,
        "hardware_measurement_map": hw_measurement_map,
    }


def classify_from_mask(mask_q0_to_qn: List[int]) -> str:
    """Deutsch-Jozsa classification for the seeded oracle f(x)=mask·x XOR b."""
    return "constant" if not any(mask_q0_to_qn) else "balanced"


def expected_input_bits_q0_to_qn(mask_q0_to_qn: List[int]) -> List[int]:
    """Expected post-DJ input-register result in q[0]...q[n-1] order."""
    if classify_from_mask(mask_q0_to_qn) == "constant":
        return [0] * len(mask_q0_to_qn)
    return list(mask_q0_to_qn)


def displayed_bitstring_from_bits(bits_q0_to_qn: List[int], measurement_map: List[List[int]]) -> str:
    n = len(bits_q0_to_qn)
    classical_bits = [0] * n
    for q_index, c_index in measurement_map:
        classical_bits[c_index] = bits_q0_to_qn[q_index]
    return "".join(str(classical_bits[i]) for i in reversed(range(n)))


def expected_display_bitstring(config: Dict[str, Any], hardware: bool = False) -> str:
    if hardware:
        bits = expected_input_bits_q0_to_qn(config["hardware_mask_q0_to_qn"])
        return displayed_bitstring_from_bits(bits, config["hardware_measurement_map"])
    bits = expected_input_bits_q0_to_qn(config["mask_q0_to_qn"])
    return displayed_bitstring_from_bits(bits, config["measurement_map"])


def expected_logical_q_string(config: Dict[str, Any], hardware: bool = False) -> str:
    mask_key = "hardware_mask_q0_to_qn" if hardware else "mask_q0_to_qn"
    bits = expected_input_bits_q0_to_qn(config[mask_key])
    return "".join(str(bits[i]) for i in reversed(range(len(bits))))


def build_oracle(qc, input_qubits, output_qubit, mask_q0_to_qn: List[int], output_offset: int):
    """Append the seeded oracle U_f: |x,y> -> |x, y XOR f(x)> to qc."""
    if output_offset == 1:
        qc.x(output_qubit)
    for i, bit in enumerate(mask_q0_to_qn):
        if bit == 1:
            qc.cx(input_qubits[i], output_qubit)
    return qc


def build_deutsch_jozsa_circuit(config: Dict[str, Any], hardware: bool = False):
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

    if hardware:
        n = config["hardware_num_input_qubits"]
        mask = config["hardware_mask_q0_to_qn"]
        output_offset = config["hardware_output_offset"]
        measurement_map = config["hardware_measurement_map"]
    else:
        n = config["num_input_qubits"]
        mask = config["mask_q0_to_qn"]
        output_offset = config["output_offset"]
        measurement_map = config["measurement_map"]

    q = QuantumRegister(n + 1, "q")
    c = ClassicalRegister(n, "c")
    qc = QuantumCircuit(q, c)
    output = q[n]

    # Prepare output qubit in |->.
    qc.x(output)
    qc.h(output)

    # Prepare input qubits in uniform superposition.
    for i in range(n):
        qc.h(q[i])

    qc.barrier()
    build_oracle(qc, [q[i] for i in range(n)], output, mask, output_offset)
    qc.barrier()

    # Interference step.
    for i in range(n):
        qc.h(q[i])

    qc.barrier()
    for q_index, c_index in measurement_map:
        qc.measure(q[q_index], c[c_index])

    return qc


def simulate_reference_counts(config: Dict[str, Any], shots: int = 2048, hardware: bool = False) -> Dict[str, int]:
    from qiskit import transpile
    from qiskit_aer import AerSimulator

    qc = build_deutsch_jozsa_circuit(config, hardware=hardware)
    sim = AerSimulator(seed_simulator=config["seed"] % (2**32 - 1))
    tqc = transpile(qc, sim, seed_transpiler=config["seed"] % (2**32 - 1))
    result = sim.run(tqc, shots=shots).result()
    return {str(k): int(v) for k, v in result.get_counts().items()}


def reference_answers(student_id: str, shots: int = 2048, assignment_id: str = "HW3") -> Dict[str, Any]:
    config = generate_config(student_id, assignment_id)
    expected_display = expected_display_bitstring(config)
    expected_logical = expected_logical_q_string(config)
    classification = classify_from_mask(config["mask_q0_to_qn"])
    counts = {expected_display: shots}
    return {
        "assignment_id": assignment_id,
        "student_id": student_id,
        "seed": config["seed"],
        "num_input_qubits": config["num_input_qubits"],
        "shots": shots,
        "mask_q0_to_qn": config["mask_q0_to_qn"],
        "output_offset": config["output_offset"],
        "measurement_mode": config["measurement_mode"],
        "measurement_map": config["measurement_map"],
        "predicted_oracle_classification": classification,
        "expected_logical_qn_to_q0": expected_logical,
        "expected_display_bitstring": expected_display,
        "simulator_counts": counts,
        "dominant_bitstring": expected_display,
    }


def validate_answers(student_answers: Dict[str, Any], student_id: str, assignment_id: str = "HW3") -> Dict[str, Any]:
    ref = reference_answers(student_id, shots=int(student_answers.get("shots", 2048)), assignment_id=assignment_id)
    feedback = []
    score = 0
    total = 9

    def check(field, points=1):
        nonlocal score
        if student_answers.get(field) == ref.get(field):
            score += points
            feedback.append(f"PASS: {field}")
        else:
            feedback.append(f"FAIL: {field}: expected {ref.get(field)!r}, got {student_answers.get(field)!r}")

    for field in [
        "seed", "num_input_qubits", "mask_q0_to_qn", "output_offset",
        "measurement_map", "predicted_oracle_classification",
        "expected_logical_qn_to_q0", "expected_display_bitstring", "dominant_bitstring"
    ]:
        check(field)

    counts = student_answers.get("simulator_counts", {})
    expected = ref["expected_display_bitstring"]
    shots = int(student_answers.get("shots", 2048))
    if isinstance(counts, dict) and int(counts.get(expected, 0)) >= int(0.95 * shots):
        score += 1
        total += 1
        feedback.append("PASS: simulator_counts has expected bitstring with at least 95% of shots")
    else:
        total += 1
        feedback.append(f"FAIL: simulator_counts should be dominated by {expected!r}")

    # Reflection fields: check presence rather than grade content automatically.
    for field in ["reflection_oracle_classification", "reflection_bit_order", "reflection_hardware_noise"]:
        total += 1
        if isinstance(student_answers.get(field), str) and len(student_answers[field].strip()) >= 40:
            score += 1
            feedback.append(f"PASS: {field} present")
        else:
            feedback.append(f"WARN/FAIL: {field} missing or too short")

    return {
        "score": score,
        "total": total,
        "passed": score == total,
        "feedback": feedback,
        "reference_core": ref,
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("student_id")
    parser.add_argument("--shots", type=int, default=2048)
    args = parser.parse_args()
    print(json.dumps(reference_answers(args.student_id, shots=args.shots), indent=2))
