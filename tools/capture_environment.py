"""Capture Python, Qiskit, and pip environment information for final project evidence."""
from __future__ import annotations

import importlib.metadata as md
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_DIR = ROOT / "environment"
ENV_DIR.mkdir(exist_ok=True)


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}")


python_info = "\n".join(
    [
        f"Python executable: {sys.executable}",
        f"Python version: {sys.version}",
        f"Platform: {platform.platform()}",
        f"Machine: {platform.machine()}",
    ]
)
write(ENV_DIR / "python_version.txt", python_info + "\n")

packages = [
    "qiskit",
    "qiskit-aer",
    "qiskit-ibm-runtime",
    "matplotlib",
    "pylatexenc",
    "jsonschema",
    "nbformat",
    "nbconvert",
    "pandas",
]
lines = []
for package in packages:
    try:
        lines.append(f"{package}=={md.version(package)}")
    except md.PackageNotFoundError:
        lines.append(f"{package}: not installed")
write(ENV_DIR / "qiskit_version_info.txt", "\n".join(lines) + "\n")

result = subprocess.run(
    [sys.executable, "-m", "pip", "freeze"],
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    check=False,
)
write(ENV_DIR / "pip_freeze.txt", result.stdout)
