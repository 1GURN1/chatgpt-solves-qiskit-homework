# Autograding and Hidden Reference Generation

## Purpose

This document explains the hidden reference generation approach used in the assignment packages.

## What hidden reference generation means

Instead of manually storing the correct answer for every student, the instructor provides a deterministic reference function. The function takes the same student ID and assignment ID used by the student and regenerates the correct assignment configuration and expected output.

This allows every student to receive a personalized version while the assignment remains autogradable.

## Common file pattern

Each assignment package follows this structure:

```text
hwX_assignment_name/
├── student_hwX_template.ipynb
├── instructor_solution_hwX.ipynb
├── hwX_reference.py
├── schema_hwX.json
├── grader_hwX_demo.py
├── README_HWX.md
└── PDF instruction sheet
```

## Core reference functions

The hidden reference file usually contains functions such as:

- `generate_config(student_id)`: creates the personalized assignment instance.
- `reference_answers(student_id)`: computes the expected instructor-side answer.
- `validate_answers(student_answers, student_id)`: compares submitted JSON to the hidden reference.
- `schema_hwX.json`: checks that required fields and types are present.
- `grader_hwX_demo.py`: demonstrates how a simple autograder can validate `answers.json`.

## Student-visible vs instructor-hidden logic

A major design lesson from the project is that answer-generation logic should not be fully visible in the student notebook.

The student notebook should include:

- instructions
- setup cells
- seed/config generation
- TODO sections
- hints
- export cell

The instructor/reference files should include:

- complete solution logic
- expected bitstring computation
- hidden validation functions
- reference simulator results
- grading comparisons

## Why this supports AI resilience

A generic ChatGPT answer is less useful when:

- each student receives a different seed
- the expected output depends on execution
- the expected result depends on a hidden reference function
- the submitted artifact is machine-readable
- the grader checks exact structure and values
- bit-ordering and measurement maps vary by student

## Limitations

Hidden reference generation does not make cheating impossible. A student can still use ChatGPT to generate code or explain concepts. However, the approach makes it harder to submit a fully correct answer without running and verifying the personalized assignment.