# HW1 - Seeded Circuits, Bit Flips, and Measurement Mapping

This folder contains the first homework prototype for the AI-resilient Qiskit assignment set.

## Files

- `student_hw1_seeded_measurement_template.ipynb` - student-facing Colab notebook template.
- `HW1_Seeded_Measurement_Instructions.pdf` - separate student instruction sheet.
- `instructor_solution_hw1_seeded_measurement.ipynb` - instructor reference solution notebook.
- `hw1_reference.py` - hidden reference generation and validation functions.
- `schema_hw1.json` - JSON schema for `answers.json`.

## Assignment idea

Students receive a personalized seed from their student ID. The seed controls:

- number of qubits, 4 or 5;
- initial basis-state bit pattern;
- a deterministic bit-flip mask;
- direct or reversed measurement mapping.

The student must build and run the circuit, export `answers.json`, and explain Qiskit bit ordering.

## Why this is AI-resilient

A generic text-only answer is unlikely to satisfy the autograder because the answer depends on the student-specific seed, the exact measurement map, and the simulator output. The assignment also targets common LLM/student failure modes: reversed bitstrings, wrong measurement mapping, hard-coded outputs, and missing measurements.

## Hardware extension

HW1 is primarily a simulator/autograder infrastructure assignment. A real IBM hardware extension can be added later by running the same small circuit on hardware and comparing the dominant output against the simulator. Hardware is not necessary for grading HW1.
