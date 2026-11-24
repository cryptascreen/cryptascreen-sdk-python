"""Every SDK method hits the (method, path) of the operation table; behaviours of the special methods."""

from __future__ import annotations

import json
from contextlib import suppress
from pathlib import Path
from typing import Any

import httpx
import pytest

from cryptascreen import CryptaScreenError, ValidationError
from cryptascreen.helpers import (
    category_share_label,
    is_assessed,
    is_graph_complete,
    is_name_clear,
    sanctions_layer_complete,
)
from cryptascreen.operations import OPERATIONS
from cryptascreen.types import ScreeningResponse

from .conftest import TEST_ADDRESS, Recorder, make_client

A = TEST_ADDRESS
BODIES: dict[str, Any] = {
    "screening": {
        "screenAddress": {"address": A, "chain": "ethereum"},
        "screenBulk": {"addresses": [A], "chains": ["ethereum"]},
        "screenBulkAsync": {"addresses": [A], "chains": ["ethereum"]},
    },
    "names": {
        "screen": {"name": "Test Name"},
        "decide": {"hitId": "h", "value": "FALSE_POSITIVE", "reason": "r"},
    },
    "graph": {
        "buildGraph": {"seedAddress": A, "chain": "ethereum"},
        "exportGraph": {"seedAddress": A, "chain": "ethereum"},
        "trace": {"seedAddress": A, "chain": "ethereum"},
    },
    "cases": {
        "create": {"title": "t", "addresses": []},
        "updateStatus": {"status": "OPEN"},
        "addNote": {"content": "c"},
        "addEvidence": {"type": "NOTE", "label": "l"},
        "escalate": {"reason": "r"},
    },
    "monitoring": {
        "addWallet": {"address": A, "chain": "ethereum", "label": "t"},
        "addName": {"name": "Test Name"},
    },
    "compliance": {
        "checkTravelRule": {
            "chain": "ethereum",
            "fromAddress": A,
            "toAddress": A,
            "transferAmountUsd": 1,
        },
        "buildTravelRulePayload": {},
        "generateDac8Report": {"taxYear": 2026, "jurisdiction": "LU", "operator": {}, "users": []},
    },
}
ARGS = {
    "chain": "ethereum",
    "address": A,
    "jobId": "job-1",
    "evaluationId": "ev-1",
    "screeningId": "sc-1",
    "caseId": "case-1",
    "id": "7",
    "webhookId": "wh-1",
    "vaspId": "v1",
}


def _call(client: Any, res: str, name: str, op: tuple) -> Any:
    ts = op[2]
    spec = _op_spec(res, ts)
    fn = getattr(getattr(client, res), name)
    args = [ARGS[p] for p in spec["p"]]
    if spec.get("body"):
        args.append(BODIES[res][ts])
    if res == "cases" and ts == "setAssignee":
        args = ["case-1", 5]
    if res == "cases" and ts == "linkEvaluation":
        args = ["case-1", "ev-1"]
    return fn(*args)


def _op_spec(res: str, ts: str) -> dict[str, Any]:
    p = Path(__file__).parent / "fixtures" / "ops_spec.json"
    spec = json.loads(p.read_text(encoding="utf-8"))
    return next(o for o in spec[res] if o["ts"] == ts)


REQUEST_OPS = [o for o in OPERATIONS if o[3] is not None]


@pytest.mark.parametrize("op", REQUEST_OPS, ids=[f"{o[0]}.{o[1]}" for o in REQUEST_OPS])
def test_method_hits_its_operation(op: tuple) -> None:
    res, name, _ts, http_method, path = op
    r = Recorder([httpx.Response(200, json={})])
    client = make_client(r)
    _call(client, res, name, op)
    assert r.requests, "no request made"
    req = r.requests[-1]
    assert req.method == http_method
    expected = "/api/v1" + path
    for k, v in ARGS.items():
        expected = expected.replace("{" + k + "}", v)
    expected = expected.replace("{caseId}", "case-1").replace("{jobId}", "job-1")
    assert req.url.path == expected


def test_screen_address_body() -> None:
    r = Recorder([httpx.Response(200, json={})])
    c = make_client(r)
    from cryptascreen.types import ScreenAddressRequest

    with suppress(Exception):
        c.screening.screen_address(
            ScreenAddressRequest(address=A, chain="ethereum", force_refresh=True)
        )
    assert json.loads(r.last.content) == {"address": A, "chain": "ethereum", "forceRefresh": True}


def test_bulk_sync_forces_async_false_and_async_true_with_idempotency_key() -> None:
    r = Recorder(
        [
            httpx.Response(200, json=[]),
            httpx.Response(200, json={"jobId": "j", "status": "PENDING", "total": 1}),
        ]
    )
    c = make_client(r)
    c.screening.screen_bulk({"addresses": [A], "chains": ["ethereum"], "async": True})
    assert json.loads(r.requests[0].content)["async"] is False
    assert "idempotency-key" not in r.requests[0].headers
    with suppress(Exception):
        c.screening.screen_bulk_async(
            {"addresses": [A], "chains": ["ethereum"], "async": False}, idempotency_key="idem-1"
        )
    assert json.loads(r.requests[1].content)["async"] is True
    assert r.requests[1].headers["idempotency-key"] == "idem-1"


def test_bulk_async_generates_one_key_kept_across_retries() -> None:
    r = Recorder([httpx.Response(503), httpx.Response(200, json={})])
    c = make_client(r)
    with suppress(Exception):
        c.screening.screen_bulk_async({"addresses": [A], "chains": ["ethereum"]})
    keys = {q.headers["idempotency-key"] for q in r.requests}
    assert len(r.requests) == 2 and len(keys) == 1 and len(next(iter(keys))) == 36


def test_job_results_normalises_spring_page_and_defaults() -> None:
    r = Recorder(
        [
            httpx.Response(
                200,
                json={
                    "content": [{"address": A}],
                    "number": 3,
                    "totalElements": 9,
                    "totalPages": 2,
                },
            )
        ]
    )
    page = make_client(r).screening.get_job_results("job-1", page=3, size=5)
    assert (page.job_id, page.page, page.size, page.total_items, page.total_pages) == (
        "job-1",
        3,
        5,
        9,
        2,
    )
    assert r.last.url.params["page"] == "3" and r.last.url.params["size"] == "5"
    r2 = Recorder([httpx.Response(200, json={})])
    p2 = make_client(r2).screening.get_job_results("job-1")
    assert (p2.items, p2.page, p2.size, p2.total_items, p2.total_pages) == ([], 0, 100, 0, 1)


def test_bulk_and_wait_polls_until_terminal() -> None:
    seq = [
        httpx.Response(200, json={"jobId": "j1", "status": "PENDING", "total": 1}),
        httpx.Response(200, json={"jobId": "j1", "status": "PROCESSING", "total": 1}),
        httpx.Response(200, json={"jobId": "j1", "status": "SOMETHING_NEW", "total": 1}),
        httpx.Response(200, json={"jobId": "j1", "status": "COMPLETED", "total": 1}),
    ]
    r = Recorder(seq)
    job = make_client(r).screening.screen_bulk_and_wait(
        {"addresses": [A], "chains": ["ethereum"]}, poll_interval=0.0, timeout=5
    )
    assert job.status == "COMPLETED"
    assert r.calls == ["POST /api/v1/screen/bulk"] + ["GET /api/v1/screen/jobs/j1"] * 3


def test_bulk_and_wait_times_out() -> None:
    r = Recorder([httpx.Response(200, json={"jobId": "j1", "status": "PENDING", "total": 1})])
    with pytest.raises(TimeoutError):
        make_client(r).screening.screen_bulk_and_wait(
            {"addresses": [A], "chains": ["ethereum"]}, poll_interval=0.0, timeout=0.05
        )


def test_query_params_are_camel_case_booleans_lowercase_and_none_dropped() -> None:
    r = Recorder([httpx.Response(200, json={})])
    with suppress(Exception):
        make_client(r).screening.get_counterparties(
            "ethereum", A, page=1, listed_only=True, days=None
        )
    q = dict(r.last.url.params)
    assert q == {"page": "1", "listedOnly": "true"}


def test_path_segments_are_url_encoded() -> None:
    r = Recorder([httpx.Response(200, json={})])
    with suppress(Exception):
        make_client(r).cases.get("a/b c")
    assert "/api/v1/cases/a%2Fb%20c" in str(r.last.url)


def test_names_screen_idempotency_header_and_history_limit() -> None:
    r = Recorder([httpx.Response(200, json={})])
    c = make_client(r)
    with suppress(Exception):
        c.names.screen({"name": "Test Name"}, idempotency_key="k1")
    assert r.last.headers["idempotency-key"] == "k1"
    c.names.history()
    assert r.last.url.params["limit"] == "50"
    c.names.decision_audit(format="csv")
    assert r.last.url.params["format"] == "csv"


def test_alert_acknowledge_trims_note_or_sends_empty_object() -> None:
    r = Recorder([httpx.Response(200, json={})])
    c = make_client(r)
    for note, expected in [("  looked at it ", {"note": "looked at it"}), ("   ", {}), (None, {})]:
        with suppress(Exception):
            c.alerts.acknowledge(7, note)
        assert json.loads(r.last.content) == expected
    assert r.last.url.path == "/api/v1/alerts/7/acknowledge"


def test_case_assignee_null_and_link_evaluation_bodies() -> None:
    r = Recorder([httpx.Response(200, json={})])
    c = make_client(r)
    for call, body in [
        (lambda: c.cases.set_assignee("c1", None), {"userId": None}),
        (lambda: c.cases.link_evaluation("c1", "ev"), {"evaluationId": "ev"}),
    ]:
        with suppress(Exception):
            call()
        assert json.loads(r.last.content) == body


def test_dac8_old_shape_is_rejected_client_side_without_a_request() -> None:
    r = Recorder()
    with pytest.raises(ValidationError) as ei:
        make_client(r).compliance.generate_dac8_report(
            {"periodStart": "2025-01-01", "addresses": []}
        )
    assert ei.value.validation_code == "DAC8_REQUEST_SHAPE"
    assert set(ei.value.field_errors) == {"taxYear", "jurisdiction", "operator", "users"}
    assert not r.requests


def test_vasp_info_unavailable_and_entity_labels() -> None:
    r = Recorder([httpx.Response(200, json={"not": "a list"})])
    c = make_client(r)
    with pytest.raises(CryptaScreenError) as ei:
        c.intelligence.get_vasp_info("v1")
    assert ei.value.code == "ENDPOINT_NOT_AVAILABLE" and ei.value.status == 0 and not r.requests
    assert c.intelligence.get_entity_labels("ethereum", A) == []
    assert c.intelligence.get_entity_label(A, "ethereum") is None
    assert r.last.url.path.endswith(f"/intelligence/entity/ethereum/{A}")


def test_webhook_management_that_needs_a_signed_in_user_is_not_offered() -> None:
    """Registering, deleting and test-sending webhooks are session-only in the API (an API key gets 403)."""
    from cryptascreen.resources.webhooks import AsyncWebhooksResource, WebhooksResource

    for cls in (WebhooksResource, AsyncWebhooksResource):
        for name in ("create", "delete", "test"):
            assert not hasattr(cls, name)


def test_helpers() -> None:
    assert is_assessed(
        ScreeningResponse.model_validate(
            {
                "chain": "ethereum",
                "address": A,
                "riskLevel": "LOW",
                "riskScore": 3,
                "sanctionsMatch": False,
            }
        )
    )
    unknown = ScreeningResponse.model_validate(
        {
            "chain": "x",
            "address": A,
            "riskLevel": "UNKNOWN",
            "riskScore": None,
            "sanctionsMatch": False,
        }
    )
    assert not is_assessed(unknown) and not sanctions_layer_complete(unknown)
    from cryptascreen.types import GraphResponse, NameScreenResponse, WalletCategoryPart

    assert is_name_clear(NameScreenResponse.model_construct(outcome="CLEAR"))
    assert not is_name_clear(NameScreenResponse.model_construct(outcome="SOMETHING_NEW"))
    g = GraphResponse.model_construct(stats=None)
    assert not is_graph_complete(g)
    part = lambda **k: WalletCategoryPart.model_construct(byAsset=[], **k)
    assert category_share_label(part(state="NOT_ANALYZED", usd_share=None)) == "n/a"
    assert category_share_label(part(state="COMPLETE", usd_share="0.1234")) == "12.3%"
    assert category_share_label(part(state="PARTIAL", usd_share=0.5), 0) == "≥ 50%"


CHAIN_REQUIRED_BODY = {
    "error": "VALIDATION_ERROR",
    "code": "CHAIN_REQUIRED",
    "field": "chain",
    "message": "chain is required: an address does not identify its network",
}


@pytest.mark.parametrize("chain", [None, "", "   "])
def test_screen_address_requires_chain(chain: str | None) -> None:
    r = Recorder([httpx.Response(200, json={})])
    body: dict[str, Any] = {"address": A}
    if chain is not None:
        body["chain"] = chain
    with pytest.raises(ValidationError) as ei:
        make_client(r).screening.screen_address(body)
    assert ei.value.validation_code == "CHAIN_REQUIRED"
    assert ei.value.status == 400
    assert r.requests == [], "nothing is sent without a chain"


def test_screen_address_model_requires_chain() -> None:
    from pydantic import ValidationError as ModelError

    from cryptascreen.types import ScreenAddressRequest

    with pytest.raises(ModelError):
        ScreenAddressRequest(address=A)  # type: ignore[call-arg]


@pytest.mark.parametrize("chains", [None, [], [""], ["ethereum", " "]])
@pytest.mark.parametrize("method", ["screen_bulk", "screen_bulk_async", "screen_bulk_and_wait"])
def test_bulk_requires_chain_per_item(method: str, chains: list[str] | None) -> None:
    r = Recorder([httpx.Response(200, json=[])])
    body: dict[str, Any] = {"addresses": [A, A]}
    if chains is not None:
        body["chains"] = chains
    with pytest.raises(ValidationError) as ei:
        getattr(make_client(r).screening, method)(body)
    assert ei.value.validation_code == "CHAIN_REQUIRED"
    assert r.requests == []


def test_server_chain_required_is_mapped() -> None:
    r = Recorder([httpx.Response(400, json=CHAIN_REQUIRED_BODY)])
    with pytest.raises(ValidationError) as ei:
        make_client(r).screening.screen_address({"address": A, "chain": "ethereum"})
    assert ei.value.validation_code == "CHAIN_REQUIRED"


def test_explicit_chain_is_sent_unchanged() -> None:
    r = Recorder([httpx.Response(200, json={}), httpx.Response(200, json=[])])
    c = make_client(r)
    with suppress(Exception):
        c.screening.screen_address({"address": A, "chain": "polygon"})
    assert json.loads(r.last.content) == {"address": A, "chain": "polygon"}
    c.screening.screen_bulk({"addresses": [A, A], "chains": ["polygon", "arb"]})
    assert json.loads(r.last.content)["chains"] == ["polygon", "arb"]
