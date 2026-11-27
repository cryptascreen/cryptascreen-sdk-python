# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Every SDK method maps to a customer API operation (HTTP method + path) - fails if not.

``tests/fixtures/customer-operations.json`` lists the operations of the customer API contract (``openapi``) and the
customer routes the SDK calls that the contract does not document yet (``customerRoutesNotYetInOpenapi``): method and
path only. An SDK method outside both lists fails.
"""

from __future__ import annotations

import re

import pytest

from cryptascreen.operations import OPERATIONS

from .conftest import load_fixture

OPS = load_fixture("customer-operations.json")

# Known contract gaps: the SDK exposes them, the customer API contract does not describe them yet.
NOT_IN_OPENAPI: set[tuple[str, str]] = set()


def _norm(path: str) -> str:
    return re.sub(r"\{[^}]+\}", "{}", path)


OPENAPI = {(o.split(" ")[0], _norm(o.split(" ")[1])) for o in OPS["openapi"]}
BACKEND = {(o.split(" ")[0], _norm(o.split(" ")[1])) for o in OPS["customerRoutesNotYetInOpenapi"]}
REQUEST_OPS = [o for o in OPERATIONS if o[3] is not None]


@pytest.mark.parametrize("op", REQUEST_OPS, ids=[f"{o[0]}.{o[1]}" for o in REQUEST_OPS])
def test_operation_is_in_the_contract(op: tuple) -> None:
    res, name, _ts, http_method, path = op
    key = (http_method, _norm(path))
    if (res, name) in NOT_IN_OPENAPI:
        assert key not in OPENAPI, "now documented in OpenAPI: remove it from NOT_IN_OPENAPI"
        assert key in BACKEND, f"{key} is in neither the contract nor the known customer routes"
    else:
        assert key in OPENAPI, (
            f"{http_method} {path} is not an operation of the customer API contract"
        )


def test_known_customer_routes_are_exactly_the_gap_list() -> None:
    assert {(o[3], _norm(o[4])) for o in REQUEST_OPS if (o[0], o[1]) in NOT_IN_OPENAPI} == BACKEND


def test_known_gap_list_is_exact() -> None:
    """The documented gaps are exactly the operations that are missing in OpenAPI (no stale, no hidden entries)."""
    missing = {(o[0], o[1]) for o in REQUEST_OPS if (o[3], _norm(o[4])) not in OPENAPI}
    assert missing == NOT_IN_OPENAPI


def test_helpers_without_endpoint_are_marked() -> None:
    assert {(o[0], o[1]) for o in OPERATIONS if o[3] is None} == {
        ("screening", "screen_bulk_and_wait"),
        ("intelligence", "get_entity_label"),
        ("intelligence", "get_vasp_info"),
    }


def test_openapi_operations_the_sdk_does_not_wrap_are_the_known_list() -> None:
    """Contract operations without an SDK method: a new one fails here."""
    sdk = {(o[3], _norm(o[4])) for o in REQUEST_OPS}
    unwrapped = sorted(f"{m} {p}" for (m, p) in OPENAPI - sdk)
    assert unwrapped == sorted(OPENAPI_NOT_WRAPPED)  # every excluded operation has a reason


OPENAPI_NOT_WRAPPED = {
    # change settings: tenant administrator session only; an API key gets 403
    "PUT /settings/score-thresholds": "tenant administrator session only",
    "DELETE /settings/score-thresholds": "tenant administrator session only",
    "PUT /settings/name-matching": "tenant administrator session only",
    "DELETE /settings/name-matching": "tenant administrator session only",
    "POST /settings/name-lists": "tenant administrator session only",
    "DELETE /settings/name-lists/{}": "tenant administrator session only",
    "PUT /settings/vendor-keys/{}": "signed-in tenant administrator session only",
    "PATCH /settings/vendor-keys/{}": "signed-in tenant administrator session only",
    "DELETE /settings/vendor-keys/{}": "signed-in tenant administrator session only",
    "POST /settings/vendor-keys/{}/test": "signed-in tenant administrator session only",
}
