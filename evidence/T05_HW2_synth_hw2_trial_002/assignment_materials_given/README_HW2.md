# HW2 - Seeded QFT / inverse-QFT Hardware Recovery

This package contains the HW2 assignment artifacts:

- `student_hw2_qft_hardware_template.ipynb` - student-facing Colab/Jupyter notebook
- `HW2_QFT_Hardware_Instructions.pdf` - separate student instruction sheet
- `instructor_solution_hw2_qft_hardware.ipynb` - instructor reference notebook
- `hw2_reference.py` - hidden reference generation and validation functions
- `schema_hw2.json` - JSON schema for `answers.json`
- `grader_hw2_demo.py` - simple command-line demo grader

## Assignment concept

Students prepare a seeded computational-basis input, apply QFT, apply inverse QFT, and measure. The simulator should recover the original seeded bitstring. An optional small hardware run lets students compare ideal simulator output with noisy IBM hardware output.

## Autograded core

The core is simulator-based and deterministic:

1. Generate seeded config from `student_id` and `assignment_id`.
2. Build QFT + inverse QFT recovery circuit.
3. Compute expected displayed bitstring using the measurement map.
4. Run Aer simulator.
5. Export `answers.json`.
6. Instructor grader regenerates reference answer using `hw2_reference.py`.

## Hardware extension

The IBM hardware section is optional/structured because live hardware is not reproducible enough for exact grading. It is useful for research and reflection:

- backend name
- job ID
- raw hardware counts
- dominant hardware bitstring
- expected bitstring percentage
- original/transpiled depth
- operation counts

## Resilience layers

- Seeded personalization
- Non-palindromic input bitstrings
- Measurement-map and bit-ordering interpretation
- Required simulator execution
- JSON output
- Optional QPY circuit artifact
- Transpiler statistics
- Hardware counts and noisy-result interpretation

## Demo grading

```bash
python grader_hw2_demo.py answers.json demo_student
```
