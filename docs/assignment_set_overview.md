# Assignment Set Overview

## Purpose

This document summarizes the proposed and partially built homework assignment sequence for the AI-resilient Qiskit assignment package.

The goal is not to create assignments that make AI use impossible. The goal is to create assignments where a student must generate personalized execution artifacts, run Qiskit code, interpret results, and submit machine-readable outputs that can be checked by hidden instructor references.

## Proposed sequence

| HW | Assignment | Main concept | Hardware role | Main resilience method |
|---|---|---|---|---|
| HW1 | Seeded Circuits, Bit Flips, and Measurement Mapping | circuits, measurement, bit ordering | optional/not required | seed, bit-flip mask, measurement-map traps |
| HW2 | QFT / Inverse QFT Hardware Recovery | QFT and inverse QFT | optional structured IBM run | seeded input, non-palindromic bitstrings, hardware counts |
| HW3 | Seeded Deutsch-Jozsa | oracle classification | optional structured IBM run | seeded oracle masks, classify before building |
| HW4 | Grover Search with Custom Marked State | search and amplitude amplification | recommended for small sizes | seeded marked state, custom oracle, scaling/noise boundary |
| HW5 | Circuit Repair + Transpiler Fingerprint | debugging and validation | optional/fake backend or real backend | QPY validation, hidden tests, transpiler statistics |

## HW1: Seeded Circuits, Bit Flips, and Measurement Mapping

### Purpose

HW1 introduces the shared infrastructure used by later assignments: seeded personalization, generated circuit configuration, simulator execution, `answers.json`, and hidden reference generation.

### Student task

Students receive a seed-generated configuration containing:

- number of qubits
- initial bit pattern
- bit-flip mask
- measurement map

They prepare the input bits, apply bit flips using X gates, measure according to the map, run the simulator, and export `answers.json`.

### Resilience methods

- seeded configuration
- non-symmetric bitstrings
- measurement-map variation
- Qiskit bit-ordering explanation
- hidden reference answer generation
- JSON-based grading

### Key learning point

Qiskit displays measurement results as `c[n-1]...c[0]`, which can differ from how students naturally list qubits as `q[0]...q[n-1]`.

## HW2: QFT / Inverse QFT Hardware Recovery

### Purpose

HW2 extends the seeded structure into a real quantum algorithm. Students prepare a known input, apply QFT, apply inverse QFT, and verify that the input is recovered.

### Student task

Students:

- generate a seeded input bitstring
- build QFT and inverse QFT circuits
- apply QFT followed by inverse QFT
- measure according to a seeded measurement map
- run the simulator
- record circuit metrics
- optionally run a smaller version on IBM hardware
- export `answers.json`

### Resilience methods

- seeded input bitstring
- non-palindromic bitstrings
- measurement-map variation
- circuit depth and operation counts
- optional IBM backend/job/count evidence
- hardware noise interpretation

### Key learning point

QFT followed by inverse QFT should recover the original input in the ideal simulator, while hardware may show the expected result with additional noisy bitstrings.

## HW3: Seeded Deutsch-Jozsa

### Purpose

HW3 uses seeded oracle masks to make Deutsch-Jozsa personalized and less vulnerable to a generic ChatGPT answer.

### Student task

Students receive:

- number of input qubits
- oracle mask
- output offset
- measurement map

They first classify the oracle as constant or balanced before building it. Then they implement the oracle, build the full Deutsch-Jozsa circuit, run the simulator, interpret the result, and export `answers.json`.

### Resilience methods

- seeded oracle mask
- classify-before-building requirement
- custom oracle construction
- bit-ordering and measurement-map interpretation
- optional hardware result comparison
- hidden reference generation

### Key learning point

A nonzero oracle mask creates a balanced function, while an all-zero mask creates a constant function. The student must understand this before constructing the circuit.

## HW4: Grover Search with Custom Marked State

### Purpose

HW4 is proposed as a stronger assignment because Grover becomes more error-prone when the marked state and oracle are customized.

### Proposed student task

Students would receive a seeded marked state. They would:

- build an oracle for that state
- build the diffuser
- choose a reasonable number of Grover iterations
- run simulator
- optionally run hardware for small sizes
- scale qubit count and determine when hardware results become unclear

### Resilience methods

- custom marked state
- oracle verification
- non-palindromic bitstrings
- simulator vs hardware comparison
- noise-boundary classification

## HW5: Circuit Repair + Transpiler Fingerprint

### Purpose

HW5 is proposed as a debugging and validation assignment. Students receive a broken seeded circuit and must repair it.

### Proposed student task

Students would:

- identify the circuit issue
- repair the circuit
- submit `answers.json`
- optionally submit `circuit.qpy`
- report original and transpiled depth
- report operation counts and two-qubit gate counts
- explain the repair

### Resilience methods

- hidden functional tests
- QPY circuit validation
- transpiler fingerprinting
- backend-specific metrics
- explanation tied to actual circuit changes

## Overall assignment design philosophy

The assignment sequence builds from simple seeded bit operations to more complex algorithmic and hardware-aware tasks. The shared pattern is:

1. Generate a personalized task from a seed.
2. Build a circuit.
3. Run Qiskit.
4. Export machine-readable results.
5. Use hidden reference generation for grading.
6. Ask a short reflection tied to the student’s own output.
7. Use hardware where it adds evidence and interpretation value.