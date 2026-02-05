"""View counter service with session-based tracking."""

from typing import Set
from datetime import datetime, timedelta


class ViewCounterService:
    """Service for tracking post views with session-based deduplication."""
    
    def __init__(self):
        """Initialize view counter with in-memory session tracking."""
        # Store viewed post IDs per session: {session_id: {post_id, ...}}
        self._session_views: dict[str, Set[int]] = {}
        # Track session expiration times: {session_id: expiration_datetime}
        self._session_expires: dict[str, datetime] = {}
        # Session lifetime in hours
        self._session_lifetime_hours = 24
    
    def should_increment_view(self, post_id: int, session_id: str) -> bool:
        """
        Check if view count should be incremented for this post.
        
        Args:
            post_id: ID of the post being viewed
            session_id: Unique session identifier (from cookie or generated)
        
        Returns:
            True if this is a new view (not seen in this session), False otherwise
        """
        # Clean up expired sessions
        self._cleanup_expired_sessions()
        
        # Check if session exists
        if session_id not in self._session_views:
            # New session - create entry
            self._session_views[session_id] = {post_id}
            self._session_expires[session_id] = (
                datetime.utcnow() + timedelta(hours=self._session_lifetime_hours)
            )
            return True
        
        # Check if post was already viewed in this session
        if post_id in self._session_views[session_id]:
            return False
        
        # New view in existing session
        self._session_views[session_id].add(post_id)
        # Refresh session expiration
        self._session_expires[session_id] = (
            datetime.utcnow() + timedelta(hours=self._session_lifetime_hours)
        )
        return True
    
    def _cleanup_expired_sessions(self):
        """Remove expired sessions from memory."""
        now = datetime.utcnow()
        expired_sessions = [
            session_id
            for session_id, expires_at in self._session_expires.items()
            if expires_at < now
        ]
        
        for session_id in expired_sessions:
            self._session_views.pop(session_id, None)
            self._session_expires.pop(session_id, None)
    
    def get_session_stats(self) -> dict:
        """Get statistics about tracked sessions (for debugging)."""
        self._cleanup_expired_sessions()
        return {
            "active_sessions": len(self._session_views),
            "total_tracked_views": sum(len(views) for views in self._session_views.values()),
        }


# Global singleton instance
view_counter_service = ViewCounterService()
