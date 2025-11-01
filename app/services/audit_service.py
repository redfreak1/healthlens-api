from typing import Dict, Any, Optional
from datetime import datetime
import json

class AuditService:
    def __init__(self):
        # In production, this would write to a database or logging service
        self.audit_log = []
    
    async def log_interaction(
        self, 
        user_id: str, 
        action: str, 
        result: str,
        response_time: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Log user interactions for audit purposes"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "action": action,
                "result": result,
                "response_time_ms": round(response_time * 1000, 2),
                "metadata": metadata or {},
                "session_id": self._generate_session_id(user_id)
            }
            
            self.audit_log.append(log_entry)
            
            # In production, write to persistent storage
            print(f"AUDIT LOG: {json.dumps(log_entry)}")
            
            return True
        except Exception as e:
            print(f"Audit logging error: {e}")
            return False
    
    async def log_error(
        self, 
        user_id: str, 
        action: str, 
        error_message: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Log errors for debugging and monitoring"""
        try:
            error_entry = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "action": action,
                "error": error_message,
                "metadata": metadata or {},
                "level": "ERROR"
            }
            
            self.audit_log.append(error_entry)
            
            # In production, write to error monitoring service
            print(f"ERROR LOG: {json.dumps(error_entry)}")
            
            return True
        except Exception as e:
            print(f"Error logging failed: {e}")
            return False
    
    async def log_cache_operation(
        self, 
        operation: str, 
        cache_key: str, 
        hit: bool,
        response_time: float
    ) -> bool:
        """Log cache operations for performance monitoring"""
        try:
            cache_entry = {
                "timestamp": datetime.now().isoformat(),
                "operation": operation,
                "cache_key": cache_key,
                "cache_hit": hit,
                "response_time_ms": round(response_time * 1000, 2),
                "level": "INFO"
            }
            
            self.audit_log.append(cache_entry)
            return True
        except Exception as e:
            print(f"Cache logging error: {e}")
            return False
    
    async def get_user_activity(self, user_id: str, limit: int = 100) -> list:
        """Get recent activity for a user"""
        user_logs = [log for log in self.audit_log if log.get("user_id") == user_id]
        return sorted(user_logs, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    async def get_system_metrics(self, hours: int = 24) -> Dict[str, Any]:
        """Get system performance metrics"""
        # Calculate metrics from recent logs
        recent_logs = self._get_recent_logs(hours)
        
        total_requests = len([log for log in recent_logs if log.get("action")])
        cache_hits = len([log for log in recent_logs if log.get("result") == "cache_hit"])
        errors = len([log for log in recent_logs if log.get("level") == "ERROR"])
        
        avg_response_time = 0
        if total_requests > 0:
            response_times = [log.get("response_time_ms", 0) for log in recent_logs if log.get("response_time_ms")]
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        return {
            "period_hours": hours,
            "total_requests": total_requests,
            "cache_hit_rate": round((cache_hits / total_requests * 100) if total_requests > 0 else 0, 2),
            "error_rate": round((errors / total_requests * 100) if total_requests > 0 else 0, 2),
            "avg_response_time_ms": round(avg_response_time, 2),
            "errors": errors
        }
    
    def _generate_session_id(self, user_id: str) -> str:
        """Generate a session ID for tracking user sessions"""
        # Simple session ID based on user and current hour
        hour = datetime.now().strftime("%Y%m%d%H")
        return f"{user_id}_{hour}"
    
    def _get_recent_logs(self, hours: int) -> list:
        """Get logs from the last N hours"""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(hours=hours)
        
        return [
            log for log in self.audit_log 
            if datetime.fromisoformat(log["timestamp"]) > cutoff
        ]