# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Narrowing and display helpers (ports of the helpers exported by @cryptascreen/sdk types)."""

from __future__ import annotations

from typing import Any

from cryptascreen._util import is_terminal_job_status  # noqa: F401  (re-exported)
from cryptascreen.types._models import (
    GraphResponse,
    NameScreenResponse,
    ScreeningResponse,
    WalletCategoryPart,
)


def is_assessed(r: ScreeningResponse) -> bool:
    """True when the address was assessed (risk level is not UNKNOWN and a score exists)."""
    return r.risk_level != "UNKNOWN" and r.risk_score is not None


def sanctions_layer_complete(r: ScreeningResponse) -> bool:
    """True only when the mandatory sanctions layer was COMPLETE; anything else is not an all-clear."""
    layers: Any = r.layers
    return bool(layers and layers.sanctions and layers.sanctions.state == "COMPLETE")


def is_name_clear(r: NameScreenResponse) -> bool:
    """True only for a completed screening whose outcome is CLEAR. Anything else needs a person to look."""
    return r.outcome == "CLEAR"


def is_graph_complete(r: GraphResponse) -> bool:
    """True only when the API states the graph read was COMPLETE (null status: legacy ``truncated`` flag)."""
    s = r.stats
    if s is None:
        return False
    if s.status is not None:
        return bool(s.status == "COMPLETE")
    return s.truncated is False


def category_share_label(part: WalletCategoryPart, digits: int = 1) -> str:
    """``n/a`` for a part without numbers, ``>= x%`` (as ``≥ x%``) for a lower bound, else ``x%``. Never renders null as 0%."""
    if part.state == "NOT_ANALYZED" or part.usd_share is None:
        return "n/a"
    pct = f"{float(part.usd_share) * 100:.{digits}f}%"
    return pct if part.state == "COMPLETE" else "≥ " + pct
