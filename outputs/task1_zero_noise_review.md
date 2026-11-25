# Zero-Noise Code Review: `inputs/task1_messy_session_manager.py`

> **Execution Note:** `ocr review --audience agent` exited with code 1 (`Error: D:\Ray Codes\AG Projects\Open Code Review github is not a git repository`), and no OCR LLM provider is configured (`~/.opencodereview/config.json` is absent; local Ollama at `http://localhost:11434` is unreachable). The findings below are verified directly against `inputs/task1_messy_session_manager.py` via host-agent review.

**Target:** `inputs/task1_messy_session_manager.py` (73 lines)  
**Findings:** 3 verified high-confidence bugs (0 style nitpicks)

---

## 1. [Critical / Security] SQL Injection in `authenticate_raw_token`
- **Location:** `inputs/task1_messy_session_manager.py:71-72`
- **Issue:** `raw_token_key` is interpolated directly into the SQL query string via an f-string before `db_cursor.execute(query)`. A crafted token value (e.g., `' OR '1'='1`) can bypass token verification or inject arbitrary SQL.
- **Diff Patch:**
```diff
--- a/inputs/task1_messy_session_manager.py
+++ b/inputs/task1_messy_session_manager.py
@@ -68,5 +68,8 @@ class SessionManager:
         """Verify API key directly against authentication database."""
-        # CRITICAL BUG: SQL Injection via unescaped string formatting
-        # Attacker can pass `' OR '1'='1` to bypass token validation
-        query = f"SELECT user_id, role, permissions FROM api_tokens WHERE token_key = '{raw_token_key}'"
-        return await db_cursor.execute(query)
+        query = (
+            "SELECT user_id, role, permissions "
+            "FROM api_tokens WHERE token_key = ?"
+        )
+        return await db_cursor.execute(query, (raw_token_key,))
```
*(Use `%s` instead of `?` if your async DB driver uses `format`/`pyformat` placeholders.)*

---

## 2. [High / Security & Correctness] Predictable / Colliding Session IDs in `register_session`
- **Location:** `inputs/task1_messy_session_manager.py:36`
- **Issue:** `session_id = f"sess_{user_id}_{int(time.time())}"` uses 1-second integer timestamp granularity. Two registrations for the same `user_id` within the same second collide and silently overwrite the earlier session. The ID format is also predictable, enabling session guessing.
- **Diff Patch:**
```diff
--- a/inputs/task1_messy_session_manager.py
+++ b/inputs/task1_messy_session_manager.py
@@ -5,6 +5,7 @@ Session Manager Service - Production User Authentication & Token Store
 import asyncio
+import secrets
 import time
 import logging
```
```diff
--- a/inputs/task1_messy_session_manager.py
+++ b/inputs/task1_messy_session_manager.py
@@ -34,6 +34,6 @@ class SessionManager:
     async def register_session(self, user_id: str, payload: Dict[str, Any]) -> str:
         """Register a new user session."""
-        session_id = f"sess_{user_id}_{int(time.time())}"
+        session_id = f"sess_{user_id}_{secrets.token_urlsafe(24)}"
         session_data = {
```

---

## 3. [High / Concurrency] Unsynchronized Mutation of `self.active_sessions`
- **Location:** `inputs/task1_messy_session_manager.py:48`
- **Issue:** `register_session` writes to `self.active_sessions[session_id]` without acquiring `self.session_lock`, whereas `purge_expired` (line 57) guards access to `self.active_sessions` with `async with self.session_lock:`. All mutations to `self.active_sessions` should hold `self.session_lock` to preserve lock invariants.
- **Diff Patch:**
```diff
--- a/inputs/task1_messy_session_manager.py
+++ b/inputs/task1_messy_session_manager.py
@@ -44,8 +44,7 @@ class SessionManager:
-        # CRITICAL BUG: Unsynchronized mutation of shared dictionary across concurrent coroutines.
-        # Developer forgot to wrap this in `async with self.session_lock:`.
-        # Under concurrent load, mutating active_sessions while another coroutine iterates causes
-        # RuntimeError: dictionary changed size during iteration or corrupts shared memory state.
-        self.active_sessions[session_id] = session_data
+        async with self.session_lock:
+            self.active_sessions[session_id] = session_data
 
         return session_id
```
