# LLM Boundaries and Failure Points Observed

## Purpose

This document records the observed limits of ChatGPT in quantum programming tasks. The goal is not to claim that ChatGPT cannot help, but to identify where it becomes unreliable or where students still need real understanding.

## No strict qubit limit for code generation

ChatGPT does not have a simple fixed qubit limit. It can write code for circuits with 3, 5, 10, or more qubits. However, being able to write code does not mean the circuit is practical or the result will be meaningful.

As qubits increase:

- simulator memory requirements grow
- hardware noise increases
- circuit depth often increases
- transpilation becomes more complex
- backend connectivity matters more
- results become harder to interpret

## Hardware results cannot be known without execution

ChatGPT can predict theoretical results, but it cannot know the actual IBM hardware result unless the job is run. Actual results depend on:

- backend selected
- calibration at the time of execution
- transpiled circuit
- shot count
- gate errors
- readout errors
- queue and runtime behavior

This makes hardware output a useful evidence layer. Asking a student to provide screenshots of their execution results could be a useful approach to this.

## Bit-ordering confusion

One common failure point is interpreting Qiskit bitstrings. Qiskit displays counts in classical-bit order `c[n-1]...c[0]`, which may differ from the logical qubit order or the way a student writes `q[0]...q[n-1]`.

Assignments can expose this weakness by using:

- non-palindromic bitstrings
- custom measurement maps
- reversed measurement order
- required explanations of qubit-to-classical-bit mapping

## Custom oracle construction

ChatGPT is more reliable for textbook circuits than for custom oracles. It becomes more error-prone when asked to build:

- Grover oracles for custom marked states
- Deutsch-Jozsa oracles with masks
- reversible Boolean functions
- circuits requiring uncomputation
- multi-controlled gates with ancillas(auxillary qubits used temporarily in quantum calculations)

## Outdated Qiskit and IBM Runtime syntax

ChatGPT may generate old Qiskit syntax or old IBM Quantum workflows. Even some of the qiskit jupiter notebooks and their original counterparts have become outdated requiring updates and review to bring them to working condition. Common issues include:

- old `IBMQ` imports
- outdated `execute()` usage
- Sampler V1 vs Sampler V2 confusion
- missing `qiskit-aer` installation
- missing `pylatexenc` for `qc.draw("mpl")`
- result extraction errors due to classical register naming

## Noisy result interpretation

ChatGPT can explain noise generically, but ambiguous hardware histograms require judgment. A strong assignment should require students to classify hardware results as successful, partial, inconclusive, or failed based on their actual counts.

## Summary

ChatGPT’s main limits are not simple inability to write quantum code. The limits appear when the task requires:

- actual hardware results
- current API usage
- backend-specific data
- correct bit-ordering interpretation
- custom oracle correctness
- scaling and noise-boundary analysis
- proof that the circuit matches the intended algorithm