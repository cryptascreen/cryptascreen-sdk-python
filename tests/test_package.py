# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Packaging consistency."""

from __future__ import annotations

import re
from pathlib import Path

import cryptascreen


def test_version_matches_pyproject() -> None:
    text = (Path(__file__).parent.parent / "pyproject.toml").read_text(encoding="utf-8")
    m = re.search(r'(?m)^version = "([^"]+)"', text)
    assert m and m.group(1) == cryptascreen.__version__


def test_examples_have_no_hardcoded_keys() -> None:
    for f in (Path(__file__).parent.parent / "examples").glob("*.py"):
        body = f.read_text(encoding="utf-8")
        assert "csk_" not in body.replace("csk_...", "") or "os.environ" in body, f
