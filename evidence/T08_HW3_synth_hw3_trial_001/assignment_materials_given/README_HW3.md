# HW3 - Seeded Deutsch-Jozsa Oracle Classification

This package contains a student-facing Deutsch-Jozsa assignment and instructor/autograder support files.

## Files

- `student_hw3_seeded_deutsch_jozsa_template.ipynb` - student Colab/Jupyter template
- `HW3_Seeded_Deutsch_Jozsa_Instructions.pdf` - PDF handout
- `instructor_solution_hw3_seeded_deutsch_jozsa.ipynb` - instructor solution notebook
- `hw3_reference.py` - hidden reference generation and validation functions
- `schema_hw3.json` - expected `answers.json` schema
- `grader_hw3_demo.py` - simple command-line grader

## Assignment concept

Students receive a seeded oracle of the form:

`f(x) = mask · x XOR output_offset`

- If `mask` is all zeros, the oracle is constant.
- If `mask` has at least one 1, the oracle is balanced.

Students must classify the oracle before building it, implement the oracle, run Deutsch-Jozsa on an ideal simulator, interpret Qiskit bit ordering, and export `answers.json`.

## Autograding idea

The instructor/autograder does not store per-student answers. Instead, `hw3_reference.py` regenerates the assignment from the same student ID and computes the expected reference result.

Example:

```bash
python grader_hw3_demo.py answers.json demo_student
```

## Hardware extension

The student notebook includes an optional IBM hardware section for a smaller 3-input-qubit oracle. Hardware results are not exact and should be graded by presence/evidence/reflection, not exact counts.
