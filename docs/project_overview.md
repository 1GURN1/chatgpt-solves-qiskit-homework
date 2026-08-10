# Project Overview

## Original project goal

This Directed Research Project started with a goal to build AI-resilient and autogradable Qiskit homework assignments for an undergraduate quantum software development course. The original motivation behind the project was that typical homework assignments and even projects can often be completed wholly by generative AI chatbots like ChatGPT or ClaudeAI when a student provides the assignment text or files to them.

The initial project focused on creating assignments where the output is dependent on actual execution of Qiskit code. These assignments would go on to implement techniques such as seeded generation, simulator outputs, noisy simulation, JSON autogradable submission files, circuit validation, and hidden reference-generation functions. The goal in mind was not to ban AI usage, but to build the homework assignments in a way that requires students to run, review, and discuss their unique results.

Over the course of the project, the focus shifted towards a clearer finding. It was observed through various experiments and tests that ordinary Qiskit assignments and even those with basic modifications for AI-deterrence remained vulnerable to completion by a minimally engaged (“lazy”) student wanting to simply complete the tasks using ChatGPT. This changed the emphasis from only making protections to keeping track of and documenting where ordinary and somewhat protected assignments failed, then making use of such findings for the creation of better assignment architecture.

## Main highlight

Conventional Qiskit homework assignments, including assignments modified with AI-deterrence techniques, can for the most part be effectively completed by a lazy student using ChatGPT. The focus should instead be on requiring personalized execution, verification, interpretation, and in-class checks of understanding instead of trying to prevent direct usage of AI tools.

The project’s major result was found to be somewhat negative, as many of the attempted techniques of homework protection did not reliably stop the “lazy student + ChatGPT = completed assignment” scenario. However, this negative result is still useful because it guides the project toward methodological approaches that may be implemented in assignment structuring for improved defensibility.

## Research questions

### RQ1: Which Qiskit homework tasks are most suitable for AI-resilient, auto-gradable assessment?

The experiments suggested that homework tasks are more suitable when they require personalized execution products rather than just written explanations. Stronger tasks include seeded circuits, customized measurement mappings, masked oracles, simulator and hardware comparisons, QPY circuit validation, transpiler statistics, and noisy-result interpretation.

### RQ2: Can seeded, execution-dependent Qiskit assignments be made reliable and accessible in Google Colab?

The homework assignments built suggest that this is feasible for simulator-based Qiskit assignments. HW1-HW3 all followed a seed-based structure where the student used their ID number to generate a personal configuration for their assignment and hidden reference functions can regenerate the correct instructor solution.

### RQ3: Can an autograder verify circuit artifacts, expectation values, noisy-simulation summaries, and transpiler statistics with useful feedback?

This process was investigated in the current assignment packets by the creation of `answers.json`, JSON schemas, basic demo graders, and hidden reference functions. More work remains for full processing and validation, especially for noisy simulation grading, QPY validation, and larger batch testing.

### RQ4: How well do text-only LLM attempts perform when asked to solve these assignments without running Qiskit?

This research question became a central focus for the project. The experiments so far show that ChatGPT can often generate working or near-working Qiskit code for most assignments. In many cases, the code or completed files required only minor setup fixes, such as installing missing libraries or adjusting IBM Runtime syntax due to outdated approaches the LLMs take in producing code. This means that text-only LLM assistance is strong enough to complete many regular assignments unless the assignment requires very specific execution-dependent, personalized, or verification-based results that cannot be predicted reliably.

### RQ5: What design principles emerge for balancing accessibility, AI-resilience, grading reliability, and conceptual learning?

The project suggests that AI-resilient assignment design should not rely on hidden text, canary markers, vague anti-AI instructions, or image embeddings. Instead, stronger designs should make use of seeded generation, machine-readable outputs, simulator execution, hardware/noise interpretation where appropriate, short reflection questions, and in-person quizzes that connect numerical results to quantum concepts and a student’s understanding.

## Work done

### Experimental tasks

The experiments conducted included testing ChatGPT’s capabilities in aiding or completing Qiskit assignments such as:

- Quantum Phase Estimation
- Quantum Fourier Transform
- Deutsch-Jozsa
- Grover’s Algorithm
- Simulator-to-IBM-hardware conversions
- Bit ordering and measurements
- Canary-marker and hidden-instruction or embedding ideas

A key finding was the ability for ChatGPT to produce working code for both Qiskit simulator and IBM hardware for lower-to-medium level quantum algorithms that would be expected for a course of this level. For example, in the QPE experiment, the simulator result produced the expected dominant bitstring, and while the IBM hardware execution had a noisy result, the expected bitstring remained dominant. In the QFT experiment, the simulator produced the expected `101` output, and the IBM hardware run on `ibm_kingston` gave `101` as the dominant result with noise distributed among various other bitstrings.

### Assignment prototypes

Three assignment packages were developed:

1. HW1: Seeded Circuits, Bit Flips, and Measurement Mapping
2. HW2: QFT / Inverse QFT Hardware Recovery
3. HW3: Seeded Deutsch-Jozsa

The assignments formed the beginning of a tangible homework package that could be used to expand into more challenging or exploratory tasks. All assignments made use of key elements like seeded generation, guided tasks, machine-readable submission artifacts, hidden reference generation, and optional IBM hardware tasks.