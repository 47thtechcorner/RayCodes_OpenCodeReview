"""
Payment Gateway Webhook & Charge Execution
"""

import requests
import logging

logger = logging.getLogger("billing")

PAYMENT_API_URL = "https://api.payment-gateway.internal/v1/charge"

async def process_payment_charge(account_id: str, amount_cents: int, token: str) -> str:
    payload = {
        "account_id": account_id,
        "amount": amount_cents,
        "currency": "USD",
        "source": token
    }

    # CRITICAL DEFECT: CWE-755 (Unhandled Exception)
    # Network timeout or gateway 504 dropped without try/except.
    # Results in 500 error back to caller while charge might have succeeded upstream,
    # causing double-billing on retry!
    response = requests.post(PAYMENT_API_URL, json=payload, timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("transaction_id")
    else:
        raise RuntimeError(f"Payment gateway rejected charge: {response.text}")

