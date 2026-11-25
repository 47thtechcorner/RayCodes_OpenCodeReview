# Task 2: Full Directory Security Audit Report

**Target:** `inputs/legacy_service/` (`router.py`, `billing.py`, `db.py`)  
**Command:** `ocr scan --path inputs/legacy_service/`

---

## Verified Findings

| File & Line | Severity | CWE | Issue |
|---|---|---|---|
| `db.py:11` | **HIGH** | `CWE-89` | Untrusted `user_id` from `router.py` concatenated directly into SQL query |
| `billing.py:22` | **MEDIUM** | `CWE-755` | Unhandled `requests.post()` network timeout drops transaction state |

### Patch 1 — `inputs/legacy_service/db.py:11`
```diff
-    query = f"SELECT id, account_id, status FROM users WHERE id = '{user_id}' AND active = 1"
-    result = await db_cursor.execute(query)
+    query = "SELECT id, account_id, status FROM users WHERE id = %s AND active = 1"
+    result = await db_cursor.execute(query, (user_id,))
```

### Patch 2 — `inputs/legacy_service/billing.py:22`
```diff
-    response = requests.post(PAYMENT_API_URL, json=payload, timeout=5)
+    try:
+        response = requests.post(PAYMENT_API_URL, json=payload, timeout=5)
+    except requests.exceptions.RequestException as exc:
+        logger.error("Payment gateway error for %s: %s", account_id, exc)
+        raise
```

---

## Tool Powers Tested
- **Cold-Start Directory Scan**: Audited the 3-file service without any Git commit or diff history.
- **Cross-File Taint Context**: Traced `user_id` originating in `router.py` into the raw SQL string in `db.py:11`.

## Observed Weaknesses
- **Blocking Sync I/O Missed**: Flagged the missing `try/except` on `requests.post()`, but did not flag that `requests.post()` is a synchronous blocking call inside an `async def` function.
- **Latency on Large Trees**: Whole-folder `ocr scan` slows down on multi-thousand-file repos unless narrowed with `--path`.

