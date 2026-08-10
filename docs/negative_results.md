# Negative Results

## Purpose

This document summarizes the negative results from the project. A negative result means that a proposed protection method, assignment design, or assessment assumption did not work as hoped.

The main finding is that ordinary Qiskit homework assignments, and even some assignments with straightforward AI-deterrence techniques, can still be completed effectively by a minimally engaged student using ChatGPT. This result matters because it shows that many intuitive protections are not enough to ensure student understanding.

The focus is not that ChatGPT is perfect. It can make mistakes, use outdated syntax, confuse bit ordering, or fabricate expected results. However, for many standard Qiskit assignments, ChatGPT is good enough to give a student a working or nearly working solution with limited effort.

## Threat model

The practical threat model is a disengaged or “lazy” student who receives a Qiskit homework assignment and asks ChatGPT to complete it, generate code, explain results, or produce a plausible answer.

This student may not fully understand the quantum algorithm. They may simply copy code, run some cells, fix basic installation issues, and submit generated outputs.

## Negative Result 1: Standard Qiskit homework is often solvable by ChatGPT

Standard textbook-style assignments are highly vulnerable. When asked to produce Qiskit code for common quantum algorithms, ChatGPT can often generate working or near-working code.

Examples include:

- Quantum Phase Estimation
- Quantum Fourier Transform
- Deutsch-Jozsa
- Grover’s Algorithm
- simulator-based circuits
- hardware-conversion code for IBM Quantum

In the Quantum Phase Estimation experiment, ChatGPT was able to produce Qiskit-style code for both simulator and IBM hardware execution. After normal setup issues were handled, the output matched the expected theoretical result. The simulator result was clean, and the real hardware result was noisy but still had the expected bitstring as the dominant measurement.

In the QFT experiment, the simulator-only version recovered the expected bitstring `101` perfectly. The IBM hardware version produced additional noisy bitstrings, but the expected output `101` was still dominant. This means that for small circuits, requiring IBM hardware execution does not automatically prevent ChatGPT assistance.

**Takeaway:** For standard small quantum algorithms, ChatGPT can often do most of the work. A student may still need to run the code and handle setup, but the main conceptual and coding burden can be significantly reduced.

## Negative Result 2: Basic “do not use AI” instructions are not effective

A written instruction telling students not to use AI is not a technical protection. It may clarify academic integrity expectations, but it does not prevent a student from pasting the task into ChatGPT and receiving a useful response.

This type of protection depends entirely on student honesty and enforcement after the fact. It does not make the assignment itself more resistant.

**Takeaway:** AI-use policies are necessary for academic integrity, but they are not sufficient as an assignment design strategy.

## Negative Result 3: Hidden text and canary markers have limited practical value

Several protection ideas focused on hidden instructions, invisible text, canary markers, or special phrases intended to reveal that ChatGPT had processed the assignment text.

One example idea was to include a hidden marker or special phrase that ChatGPT might repeat in its answer. Another idea was to modify the final output label in a QPE notebook so that copied AI-generated responses could be identified.

These methods may sometimes detect careless AI use, but they are weak as a general defense. A student could remove suspicious text, regenerate the answer, ask ChatGPT to avoid odd phrases, or manually edit the output. The method also does not guarantee that the student understands the assignment. ChatGPT in its current form can also just identify that the instructor is trying to trap a student and inform the student going forward.

**Takeaway:** Canary markers and hidden instructions may provide evidence in some cases, but they do not reliably prevent AI-assisted completion. They are detection tricks, not strong assessment designs.

## Negative Result 4: Altered wording does not meaningfully stop ChatGPT

Changing the wording of a standard assignment does not necessarily make it resistant. If the underlying task is still a recognizable Qiskit algorithm, ChatGPT can often infer what is needed.

For example, if the assignment asks for QPE, QFT, Deutsch-Jozsa, or Grover in slightly different wording, ChatGPT can still generate a generic implementation and explanation. The student may only need to adapt small details.

**Takeaway:** Surface-level wording changes are not enough. The vulnerability comes from the generic structure of the task, not only from the exact wording.

## Negative Result 5: Simulator-only execution is not enough if the task is generic

Simulator execution improves the assignment compared with a purely written answer, but it is not enough if all students have the same task.

ChatGPT can generate simulator code for many Qiskit assignments. If the simulator result is deterministic or theoretically obvious, ChatGPT can also predict the expected output. A student can run the generated code with little understanding.

Simulator-only work becomes stronger when it is combined with:

- seeded student-specific inputs
- hidden reference generation
- machine-readable `answers.json`
- QPY circuit validation
- bit-ordering traps
- noisy simulation with tolerance
- short conceptual checks

**Takeaway:** Execution helps, but generic simulator execution is still vulnerable. Personalization and validation are needed.

## Negative Result 6: IBM hardware execution helps, but does not fully solve the problem

IBM hardware execution introduces real uncertainty:

- backend availability
- queue delay
- transpilation changes
- hardware noise
- gate errors
- readout errors
- actual raw counts
- backend-specific circuit depth

These are harder for ChatGPT to fabricate exactly. However, ChatGPT can still help significantly by writing the hardware code, explaining the expected result, and guiding result interpretation.

In the QPE and QFT experiments, ChatGPT-generated hardware code was effective enough to run small circuits. The real devices produced noisy histograms, but the expected result remained dominant. This means that hardware execution adds a useful layer, but it does not by itself guarantee AI resistance.

**Takeaway:** Real hardware is useful as an execution-dependent evidence layer, but it should be combined with reflection, simulator comparison, raw counts, backend/job documentation, and interpretation requirements.

## Negative Result 7: Too much scaffolding can give away the assignment

While building HW1, HW2, and HW3, an important design issue appeared: if the student notebook includes too much answer-generation logic, then the assignment becomes less meaningful.

For example, in HW1, if the notebook gives students the full function for computing the expected displayed bitstring, then the student does not need to reason about Qiskit bit ordering. In HW2, if the full QFT and inverse-QFT implementation is given, then the student does not have to build the main circuit logic. In HW3, if the classification and expected-output logic is fully provided, then the student does not need to understand the oracle.

**Takeaway:** Scaffolding is necessary for accessibility, but the completed answer logic should live in instructor files, not in the student template. The student notebook should provide instructions, hints, and TODO sections rather than full solution functions.

## Negative Result 8: Reflection questions alone are weak if they are generic

Short written reflection questions can support learning, but generic reflection questions are easy for ChatGPT to answer.

For example, a question such as “Explain why hardware is noisy” can be answered in a generic way without looking at the student’s actual histogram. A stronger reflection asks the student to refer to their own counts, dominant bitstring, backend, circuit depth, and whether the expected result was clearly visible.

**Takeaway:** Reflection questions should be tied to personalized execution results. Otherwise, they become another generic text task that ChatGPT can easily complete.

## Summary of methods that had limited value when used alone

- ordinary unpersonalized Qiskit homework
- basic “do not use AI” instructions
- hidden text
- canary markers
- surface-level wording changes
- generic simulator tasks
- generic reflection questions
- hardware execution without interpretation
- highly scaffolded notebooks that include answer-generation logic

## What seems more promising

The negative results suggest that stronger assignments should use multiple layers:

1. seeded personalization
2. execution-dependent outputs
3. hidden reference generation
4. `answers.json` machine-readable submissions
5. optional `circuit.qpy` validation
6. non-symmetric bitstrings to expose reversal errors
7. measurement-map variation
8. simulator vs hardware comparison
9. original vs transpiled circuit metrics
10. raw hardware counts and job IDs
11. reflection tied to the student’s own result
12. short in-class quiz or oral check

The goal is not to make AI use impossible. The goal is to make the assignment require enough real execution, interpretation, and verification that a student cannot submit a correct solution purely by copying a generic ChatGPT answer.