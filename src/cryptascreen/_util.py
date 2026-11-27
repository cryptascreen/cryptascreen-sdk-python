# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Small internal helpers shared by the resources."""

from __future__ import annotations

import uuid
from typing import Any
from urllib.parse import quote

from pydantic import BaseModel

from cryptascreen.errors import ValidationError
from cryptascreen.types._models import ScreeningJobResultsPage

TERMINAL_JOB_STATUSES = ("COMPLETED", "PARTIAL", "FAILED", "CANCELLED")


def _enc(value: str) -> str:
    """encodeURIComponent for a path segment."""
    return quote(str(value), safe="-_.!~*'()")


def _body(request: BaseModel | dict[str, Any]) -> dict[str, Any]:
    if isinstance(request, BaseModel):
        return request.model_dump(by_alias=True, exclude_none=True, mode="json")
    return dict(request)


_CHAIN_REQUIRED = "chain is required: an address does not identify its network"


def _chain_required(field: str) -> ValidationError:
    return ValidationError(
        _CHAIN_REQUIRED,
        {field: [_CHAIN_REQUIRED]},
        None,
        "CHAIN_REQUIRED",
    )


def _blank(value: Any) -> bool:
    return not isinstance(value, str) or not value.strip()


def _require_chain(body: dict[str, Any]) -> dict[str, Any]:
    """Single screening: ``chain`` must be present and non-blank (no default network)."""
    if _blank(body.get("chain")):
        raise _chain_required("chain")
    return body


def _require_chains(body: dict[str, Any]) -> dict[str, Any]:
    """Bulk screening: every address row needs a non-blank entry in ``chains``."""
    addresses = body.get("addresses") or []
    chains = body.get("chains")
    if addresses and (not isinstance(chains, list) or not chains or any(map(_blank, chains))):
        raise _chain_required("chains")
    return body


def _query(**params: Any) -> dict[str, Any]:
    """Drop None, render booleans like axios (true/false); wire names are camelCase."""
    out: dict[str, Any] = {}
    for k, v in params.items():
        if v is None:
            continue
        out[_camel(k)] = ("true" if v else "false") if isinstance(v, bool) else v
    return out


def _camel(name: str) -> str:
    head, *rest = name.split("_")
    return head + "".join(p.capitalize() for p in rest)


def generate_idempotency_key() -> str:
    """Random idempotency key (RFC 4122 v4)."""
    return str(uuid.uuid4())


def is_terminal_job_status(status: str | None) -> bool:
    """Terminal job statuses (polling stops). Unknown future values are NOT terminal."""
    return (status or "") in TERMINAL_JOB_STATUSES


def _normalise_job_results(data: Any, job_id: str, page: int, size: int) -> ScreeningJobResultsPage:
    d = data if isinstance(data, dict) else {}
    items: list[Any] = (
        d["items"]
        if isinstance(d.get("items"), list)
        else d["content"]
        if isinstance(d.get("content"), list)
        else []
    )

    def num(*vals: Any, default: int) -> int:
        for v in vals:
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                return int(v)
        return default

    return ScreeningJobResultsPage.model_validate(
        {
            "jobId": d["jobId"] if isinstance(d.get("jobId"), str) else job_id,
            "status": d["status"] if isinstance(d.get("status"), str) else None,
            "items": items,
            "page": num(d.get("page"), d.get("number"), default=page),
            "size": num(d.get("size"), default=size),
            "totalItems": num(d.get("totalItems"), d.get("totalElements"), default=len(items)),
            "totalPages": num(d.get("totalPages"), default=1),
        }
    )
