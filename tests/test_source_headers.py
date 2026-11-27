# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Every Python source file starts with the two-line copyright and SPDX licence header."""

from __future__ import annotations

from pathlib import Path

L1 = "# Copyright (c) 2024-2026 CryptaCount, Inc."
L2 = "# SPDX-License-Identifier: MIT"
ROOT = Path(__file__).resolve().parent.parent


def problem(content: str) -> str | None:
    lines = content.lstrip("\ufeff").splitlines()
    i = 0
    while i < len(lines) and (
        lines[i].startswith("#!") or "coding" in lines[i] and lines[i].startswith("#")
    ):
        i += 1
    return None if lines[i : i + 2] == [L1, L2] else "missing or wrong header"


def test_every_python_source_file_starts_with_the_header() -> None:
    files = [p for d in ("src", "tests", "examples") for p in (ROOT / d).rglob("*.py")]
    bad = [str(p.relative_to(ROOT)) for p in files if problem(p.read_text(encoding="utf-8"))]
    assert len(files) > 20
    assert bad == []


def test_the_rule_catches_a_missing_header() -> None:
    assert problem(f"{L1}\n{L2}\nimport os\n") is None
    assert problem(f"#!/usr/bin/env python3\r\n{L1}\r\n{L2}\r\n") is None
    assert problem("import os\n") is not None
    assert problem(f"# Copyright (c) 2026 Someone Else\n{L2}\n") is not None
