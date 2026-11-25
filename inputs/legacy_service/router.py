"""
Legacy Billing Microservice - Inbound API Gateway Router
"""

from .billing import process_payment_charge
from .db import fetch_user_record

class BillingRouter:
    def __init__(self, db_client):
        self.db = db_client

    async def handle_charge_request(self, payload: dict):
        user_id = payload.get("user_id")
        amount = payload.get("amount")
        payment_token = payload.get("token")

        user = await fetch_user_record(self.db, user_id)
        if not user:
            return {"status": "error", "message": "User not found"}

        result = await process_payment_charge(user["account_id"], amount, payment_token)
        return {"status": "success", "charge_id": result}

