"""Demo command-line grader for HW2.

Usage:
    python grader_hw2_demo.py answers.json demo_student
"""
import json
import sys
from hw2_reference import validate_answers

if len(sys.argv) != 3:
    raise SystemExit("Usage: python grader_hw2_demo.py answers.json STUDENT_ID")

answers_path, student_id = sys.argv[1], sys.argv[2]
with open(answers_path, "r") as f:
    answers = json.load(f)

result = validate_answers(answers, student_id)
print(json.dumps(result, indent=2))
