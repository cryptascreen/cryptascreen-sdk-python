# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Webhook verification against the shared cross-SDK vectors (tests/fixtures/webhook_vectors.json)."""

from __future__ import annotations

import pytest

from cryptascreen import (
    WebhookSignatureError,
    compute_webhook_signature,
    construct_webhook_event,
    verify_webhook_signature,
)

from .conftest import load_fixture

V = load_fixture("webhook_vectors.json")


@pytest.mark.parametrize("vec", V["sign"], ids=lambda v: f"sign-{v['timestamp']}-{len(v['body'])}")
def test_sign_vectors(vec: dict) -> None:
    assert compute_webhook_signature(vec["secret"], vec["body"], vec["timestamp"]) == vec["hex"]
    assert (
        compute_webhook_signature(vec["secret"], vec["body"].encode("utf-8"), vec["timestamp"])
        == vec["hex"]
    )


@pytest.mark.parametrize("vec", V["verify"], ids=lambda v: v["name"])
def test_verify_vectors(vec: dict) -> None:
    kw = {"tolerance": vec["tolerance"], "allow_legacy": vec["allowLegacy"], "now": vec["now"]}
    if vec["expect"]["ok"]:
        assert verify_webhook_signature(vec["secret"], vec["body"], vec["headers"], **kw) is True
    else:
        with pytest.raises(WebhookSignatureError) as ei:
            verify_webhook_signature(vec["secret"], vec["body"], vec["headers"], **kw)
        assert ei.value.code == vec["expect"]["code"]


def test_bytes_body_equals_str_body() -> None:
    vec = next(v for v in V["verify"] if v["name"] == "valid-v2-unicode")
    assert verify_webhook_signature(
        vec["secret"], vec["body"].encode("utf-8"), vec["headers"], now=vec["now"]
    )


def test_construct_event_returns_parsed_payload() -> None:
    vec = next(v for v in V["verify"] if v["name"] == "valid-v2-simple")
    ev = construct_webhook_event(vec["secret"], vec["body"], vec["headers"], now=vec["now"])
    assert ev["type"] == "screening.flagged" and ev["data"]["evaluationId"] == "ev-test-1"
