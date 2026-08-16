# Controlled ChatGPT Trial Protocol

## Model and date

Use the same ChatGPT model for all nine trials. Record the exact displayed model name and UTC date in `results.csv` and each `trial_summary.md`.

## Trial isolation

Start a completely new ChatGPT conversation for every trial. Do not use memory from previous trials. Do not paste instructor solutions, hidden reference functions, expected answers, or grader feedback.

## Inputs

Provide only the student-visible assignment materials in each trial folder under `assignment_materials_given/`. Use the synthetic student ID listed in that trial folder.

## Prompt

Use the prompt in `prompt_to_use.md` for each trial.

## Follow-ups

Allow at most two follow-ups. A follow-up may only:

1. paste an exact runtime error, or
2. ask ChatGPT to provide a required file it omitted.

Do not provide conceptual hints, instructor feedback, expected answers, or independent fixes.

## Execution

Copy and execute ChatGPT's output in a clean environment. Save every generated version, traceback, command log, notebook output, and final artifact. Do not discard unsuccessful trials.

## Grading

Run the hidden grader after each final artifact is produced. Save the complete grader output. Record whether the first response executed and passed, and whether the final response executed and passed after permitted follow-ups.
