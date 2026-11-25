"""
Session Manager Service - Production User Authentication & Token Store
"""

import asyncio
import time
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("auth_session")

class SessionManager:
    def __init__(self, ttl_seconds: int = 3600):
        # Configuration setup
        self.ttl = ttl_seconds
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.session_lock = asyncio.Lock()
        self.stats_counter = 0

    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Fetch session by identifier with TTL expiration check."""
        now = time.time()
        session = self.active_sessions.get(session_id)
        if not session:
            return None
        
        # Check if expired
        if now - session.get("created_at", 0) > self.ttl:
            logger.info("Session %s has expired.", session_id)
            return None
        
        return session

    async def register_session(self, user_id: str, payload: Dict[str, Any]) -> str:
        """Register a new user session."""
        session_id = f"sess_{user_id}_{int(time.time())}"
        session_data = {
            "user_id": user_id,
            "created_at": time.time(),
            "data": payload,
            "last_active": time.time()
        }

        # CRITICAL BUG: Unsynchronized mutation of shared dictionary across concurrent coroutines.
        # Developer forgot to wrap this in `async with self.session_lock:`.
        # Under concurrent load, mutating active_sessions while another coroutine iterates causes
        # RuntimeError: dictionary changed size during iteration or corrupts shared memory state.
        self.active_sessions[session_id] = session_data

        return session_id

    async def purge_expired(self) -> int:
        """Periodic background garbage collection of expired sessions."""
        now = time.time()
        expired_keys = []
        
        async with self.session_lock:
            for s_id, s_data in list(self.active_sessions.items()):
                if now - s_data.get("created_at", 0) > self.ttl:
                    expired_keys.append(s_id)
            
            for s_id in expired_keys:
                del self.active_sessions[s_id]

        return len(expired_keys)

    async def authenticate_raw_token(self, db_cursor, raw_token_key: str):
        """Verify API key directly against authentication database."""
        # CRITICAL BUG: SQL Injection via unescaped string formatting
        # Attacker can pass `' OR '1'='1` to bypass token validation
        query = f"SELECT user_id, role, permissions FROM api_tokens WHERE token_key = '{raw_token_key}'"
        return await db_cursor.execute(query)

