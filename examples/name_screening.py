# Copyright (c) 2024-2026 CryptaCount, Inc.
# SPDX-License-Identifier: MIT
"""Sanctions name screening of a test name."""

import os

from cryptascreen import CryptaScreen
from cryptascreen.helpers import is_name_clear

with CryptaScreen(api_key=os.environ["CRYPTASCREEN_API_KEY"]) as client:
    result = client.names.screen({"name": "Test Name", "type": "PERSON"})
    print(result.outcome, "clear" if is_name_clear(result) else "needs a person to look")
