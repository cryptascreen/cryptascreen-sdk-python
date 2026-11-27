# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Screen one test address and print the result (test address only)."""

import os

from cryptascreen import CryptaScreen

with CryptaScreen(api_key=os.environ["CRYPTASCREEN_API_KEY"]) as client:
    result = client.screening.screen_address(
        {"address": "0x1111111111111111111111111111111111111111", "chain": "ethereum"}
    )
    print(result.risk_level, result.risk_score, result.sanctions_match, result.assessment_status)
