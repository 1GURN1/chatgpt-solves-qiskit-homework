#!/usr/bin/env python3
"""Demo grader for HW3 answers.json.
Usage:
    python grader_hw3_demo.py answers.json demo_student
"""
import json
import sys
from hw3_reference import validate_answers

if len(sys.argv) != 3:
    print("Usage: python grader_hw3_demo.py answers.json <student_id>")
    sys.exit(2)

answers_path, student_id = sys.argv[1], sys.argv[2]
with open(answers_path, "r", encoding="utf-8") as f:
    answers = json.load(f)

result = validate_answers(answers, student_id)
print(json.dumps(result, indent=2))
sys.exit(0 if result["passed"] else 1)
