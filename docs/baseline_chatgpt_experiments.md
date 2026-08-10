# Baseline ChatGPT and IBM Hardware Experiments

## Purpose

This document summarizes the main experiments where ChatGPT was asked to complete, assist with, or convert Qiskit homework-style assignments. These experiments support the project’s central finding: ordinary quantum computing homework tasks are often vulnerable to minimally engaged AI-assisted completion.

The experiments also considered whether requiring IBM hardware execution makes an assignment harder for ChatGPT to complete. The finding was mixed. Hardware execution adds useful real-world evidence that ChatGPT cannot exactly predict, but it does not by itself prevent ChatGPT from helping a student complete most of the assignment.

## General Pattern Observed

Across multiple experiments, ChatGPT was able to:

* identify the intended quantum algorithm from the prompt,
* generate Qiskit code for the circuit,
* generate simulator code,
* explain expected theoretical results,
* convert simulator workflows into IBM hardware workflows,
* help debug common setup issues,
* provide plausible reflection or explanation text.

The main weaknesses observed were:

* outdated Qiskit or IBM Runtime syntax,
* missing package installation instructions,
* bit-ordering confusion,
* overly confident interpretation of noisy hardware results,
* occasional changes to the intended circuit when rewriting code,
* inability to know actual hardware results before execution.

Overall, ChatGPT was strong enough to complete or nearly complete many standard Qiskit assignments at the scale normally used in an undergraduate quantum computing course.

## Why IBM Hardware Was Tested

A major question in the project was whether real quantum hardware could make assignments more AI-resilient. IBM hardware introduces execution-dependent variables that ChatGPT cannot exactly predict, including:

* selected backend,
* job ID,
* queue delay,
* live calibration conditions,
* backend topology,
* transpiled circuit depth,
* hardware gate errors,
* readout errors,
* noisy raw counts.

These factors make hardware results harder to fabricate exactly than ideal simulator results. However, ChatGPT can still help with much of the assignment, including writing Runtime code, selecting backend logic, building and transpiling circuits, retrieving counts, plotting histograms, explaining theoretical expected results, and writing reflection text.

Therefore, hardware should be treated as an evidence and interpretation layer rather than a complete AI-proofing method.

## Experiment 1: Quantum Phase Estimation

### Task

The Quantum Phase Estimation experiment tested whether ChatGPT could produce simulator and IBM hardware code for a QPE assignment.

### ChatGPT Result

ChatGPT was able to produce Qiskit-style code for both simulator and IBM hardware execution. After normal setup issues were handled, the code was able to run.

### Simulator Result

The simulator produced the expected dominant bitstring. The expected phase calculation matched the theoretical result for the tested assignment.

### Hardware Result

The IBM hardware result was noisier than the simulator result, but the expected bitstring remained dominant.

### Takeaway

QPE did not appear to be resistant to ChatGPT assistance at the small scale tested. ChatGPT could generate working or near-working code, and the hardware result remained interpretable. Real hardware introduced noise, but it did not prevent the correct result from being identified.

## Experiment 2: Quantum Fourier Transform

### Task

The QFT experiment used an inverse-QFT recovery test. A known input bitstring was prepared, QFT was applied, inverse QFT was applied, and the circuit was measured. This produced a clear expected output for simulator and hardware comparison.

### Simulator Result

The simulator produced the expected output `101` in all 4096 shots.

### Hardware Result

The IBM hardware version ran on `ibm_kingston`. The expected result `101` remained dominant with 3709 out of 4096 shots, or about 90.55%. The remaining shots were distributed across other bitstrings due to hardware noise.

### Transpilation Observation

The original circuit depth was 10, while the transpiled circuit depth increased to 32. This shows that the hardware version is not simply the abstract circuit. It is transformed into backend-supported operations, introducing additional opportunities for noise.

### Takeaway

ChatGPT could generate useful simulator and hardware QFT code. The hardware comparison added meaningful execution evidence, but it did not stop ChatGPT from assisting with the assignment. For this small QFT example, hardware noise did not obscure the correct answer.

## Experiment 3: Deutsch-Jozsa

### Task

The Deutsch-Jozsa work focused on both a standard course notebook and a redesigned seeded version with custom oracle masks.

### ChatGPT Result

For a standard Deutsch-Jozsa task, ChatGPT can generally produce the standard algorithm structure:

1. prepare input qubits in superposition,
2. prepare the output qubit in `|->`,
3. apply the oracle,
4. apply Hadamards to the input register,
5. measure input qubits,
6. classify the oracle as constant or balanced.

### More Resilient Redesign

The seeded Deutsch-Jozsa assignment made the task more personalized by assigning each student an oracle mask. The mask determines which input qubits control the output qubit. This makes a generic Deutsch-Jozsa solution less sufficient because the student must use their specific oracle configuration.

The assignment also asks students to classify the oracle before building it. This forces them to decide whether the seeded oracle is constant or balanced based on the configuration, rather than simply running code and copying the output.

### Hardware Role

The simulator portion remains the reliable autograded core. The hardware section can be used optionally or as a research extension, where students record backend name, job ID, raw counts, dominant bitstring, and classification under noise.

### Takeaway

Generic Deutsch-Jozsa is easy for ChatGPT. Seeded masked oracles improve the assignment by forcing student-specific circuit construction and interpretation. Hardware can add useful evidence, but exact hardware counts should not be graded rigidly.

## Experiment 4: Grover’s Algorithm

### Task

Grover was discussed as a planned or partially explored assignment direction rather than a fully completed package.

### Expected Vulnerability

A basic Grover example with one marked state is still within ChatGPT’s capabilities. ChatGPT can often write a standard oracle and diffuser for small examples.

### More Resilient Version

A stronger Grover assignment would use:

* seeded marked states,
* custom oracle construction,
* non-palindromic bitstrings,
* scaling from 3 to 5 or more qubits,
* simulator vs hardware comparison,
* classification of hardware results as successful, partial, inconclusive, or failed.

### Takeaway

Grover becomes more useful as an AI-resilience test when it requires custom oracle construction and scaling, rather than a standard textbook example.

## Hardware Result Classification Scheme

A useful way to discuss hardware output is to classify it as:

| Classification | Suggested rule                                           |
| -------------- | -------------------------------------------------------- |
| Successful     | Expected bitstring clearly dominant and above about 70%  |
| Partial        | Expected bitstring dominant but around 40–70%            |
| Inconclusive   | Expected bitstring is close to others or below about 40% |
| Failed         | Expected bitstring is not dominant                       |

These thresholds are not absolute, but they give students a structured way to interpret noisy hardware results.

## Overall Finding

The baseline experiments suggest that ChatGPT is strong enough to complete many standard Qiskit assignments at the scale normally used in an undergraduate course. It may not always produce perfect code, but it can usually get close enough that a student only needs minor debugging or setup work.

IBM hardware execution adds useful evidence because it requires real backend data, job IDs, transpilation metrics, and noisy counts that ChatGPT cannot know in advance. However, ChatGPT can still generate code and theoretical interpretations. Therefore, hardware should be combined with seeded personalization, simulator comparison, transpiler statistics, raw counts, job IDs, and reflection questions tied directly to the student’s actual result.

The main conclusion is that ordinary Qiskit assignments are vulnerable, and hardware alone is not a complete solution. The stronger direction is personalized, execution-dependent, and verification-based assignment design.
