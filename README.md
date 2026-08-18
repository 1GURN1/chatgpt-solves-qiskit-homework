# CP493-DirectedResearch
# Final Reproducibility README

This repository contains the frozen assignment versions, controlled ChatGPT trial evidence, previous experiment inventory, and environment-capture files for the CP493 directed research project on AI-resilient, auto-gradable Qiskit assignments during the spring 2026 term.

## Repository contents

- `assignments_frozen/`: final frozen versions of HW1, HW2, and HW3, including student templates, instruction PDFs, schemas, hidden reference files, instructor notebooks, and demo graders.
- `evidence/`: nine controlled ChatGPT trial folders. Each folder contains the student-facing materials used, transcript/evidence files, generated versions, logs, grader output, and a short trial summary.
- `results.csv`: final controlled-trial result table.
- `previous_experiments_inventory.csv`: inventory of earlier QPE, QFT, Deutsch-Jozsa, Grover, hardware, canary-marker, hidden-text, and related tests.
- `raw_evidence_sanitized/`: retained earlier raw evidence notebooks where available. IBM tokens and personal credentials should be redacted before commit.
- `environment/`: Python, Qiskit, and package-version information captured from the environment used to rerun graders.
- `tools/`: helper scripts for environment capture and local sanitization checks.

## Environment setup

Create and activate a clean Python environment, then install the packages used by the assignments and graders:

```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install qiskit qiskit-aer qiskit-ibm-runtime matplotlib pylatexenc jsonschema nbformat nbconvert pandas
```

## Capture environment files

Run this before the final commit:

```bash
python tools/capture_environment.py
```

This writes:

- `environment/pip_freeze.txt`
- `environment/python_version.txt`
- `environment/qiskit_version_info.txt`

These files document the environment used for final grading/reproduction. If any Qiskit package is not installed, the script records that explicitly.

## Rerun controlled-trial graders

Run all hidden graders from the repository root.

### HW1

```bash
python assignments_frozen/hw1_seeded_measurement/grader_hw1_demo.py evidence/T01_HW1_synth_hw1_trial_007/generated_versions/answers.json synth_hw1_trial_007
python assignments_frozen/hw1_seeded_measurement/grader_hw1_demo.py evidence/T02_HW1_synth_hw1_trial_008/generated_versions/answers.json synth_hw1_trial_008
python assignments_frozen/hw1_seeded_measurement/grader_hw1_demo.py evidence/T03_HW1_synth_hw1_trial_009/generated_versions/answers.json synth_hw1_trial_009
```

### HW2

```bash
python assignments_frozen/hw2_qft_hardware/grader_hw2_demo.py evidence/T04_HW2_synth_hw2_trial_001/generated_versions/answers.json synth_hw2_trial_001
python assignments_frozen/hw2_qft_hardware/grader_hw2_demo.py evidence/T05_HW2_synth_hw2_trial_002/generated_versions/answers.json synth_hw2_trial_002
python assignments_frozen/hw2_qft_hardware/grader_hw2_demo.py evidence/T06_HW2_synth_hw2_trial_004/generated_versions/answers.json synth_hw2_trial_004
```

### HW3

```bash
python assignments_frozen/hw3_seeded_deutsch_jozsa/grader_hw3_demo.py evidence/T07_HW3_synth_hw3_trial_002/generated_versions/answers.json synth_hw3_trial_002
python assignments_frozen/hw3_seeded_deutsch_jozsa/grader_hw3_demo.py evidence/T08_HW3_synth_hw3_trial_001/generated_versions/answers.json synth_hw3_trial_001
python assignments_frozen/hw3_seeded_deutsch_jozsa/grader_hw3_demo.py evidence/T09_HW3_synth_hw3_trial_005/generated_versions/answers.json synth_hw3_trial_005
```

If a trial saved the final JSON under a different filename or nested folder, use that exact path and keep the evidence file unchanged to prevent further issues.

## Save grader outputs

To regenerate grader outputs, redirect each command into the matching trial folder. Example:

```powershell
python assignments_frozen/hw1_seeded_measurement/grader_hw1_demo.py evidence/T01_HW1_synth_hw1_trial_007/generated_versions/answers.json synth_hw1_trial_007 > evidence/T01_HW1_synth_hw1_trial_007/grader_output/hidden_grader_output.txt
```