"""
Database Client & User Account Lookup
"""

import logging

logger = logging.getLogger("db")

async def fetch_user_record(db_cursor, user_id: str):
    # CRITICAL DEFECT: CWE-89 (SQL Injection)
    # Untrusted user_id from API request formatted directly into SQL query
    query = f"SELECT id, account_id, status FROM users WHERE id = '{user_id}' AND active = 1"
    
    logger.debug("Executing query: %s", query)
    result = await db_cursor.execute(query)
    return await result.fetchone()

