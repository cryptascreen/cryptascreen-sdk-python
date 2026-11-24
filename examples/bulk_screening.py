"""Bulk screening of a few test addresses: synchronous, then as an asynchronous job."""

import os

from cryptascreen import CryptaScreen

ADDRESSES = [
    "0x1111111111111111111111111111111111111111",
    "0x2222222222222222222222222222222222222222",
    "0x3333333333333333333333333333333333333333",
]

with CryptaScreen(api_key=os.environ["CRYPTASCREEN_API_KEY"]) as client:
    for r in client.screening.screen_bulk(
        {"addresses": ADDRESSES, "chains": ["ethereum"] * len(ADDRESSES)}
    ):
        print(r.address, r.risk_level, r.sanctions_match)

    job = client.screening.screen_bulk_and_wait(
        {"addresses": ADDRESSES, "chains": ["ethereum"] * len(ADDRESSES)}
    )
    print(job.job_id, job.status)
