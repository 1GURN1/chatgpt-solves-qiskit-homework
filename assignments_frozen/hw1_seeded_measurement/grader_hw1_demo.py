"""Minimal HW1 grading demo.
Usage:
    python grader_hw1_demo.py answers.json demo_student
"""
import json
import sys
from hw1_reference import validate_answers

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python grader_hw1_demo.py answers.json student_id")
        raise SystemExit(2)
    path = sys.argv[1]
    student_id = sys.argv[2]
    with open(path) as f:
        answers = json.load(f)
    passed, feedback = validate_answers(answers, student_id, shots=answers.get("shots", 2048))
    print("PASSED" if passed else "FAILED")
    for msg in feedback:
        print("-", msg)
    raise SystemExit(0 if passed else 1)
