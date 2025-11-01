from app.models.schemas import PersonaType
from typing import Dict, Any, Optional
from datetime import datetime
import hashlib
import json

class BehaviorService:
    def __init__(self):
        # In production, this would connect to an analytics service
        self.behavior_data = []
    
    async def track_behavior(
        self, 
        user_id: str, 
        action: str, 
        persona: PersonaType,
        response_time: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Track user behavior with anonymized data"""
        try:
            # Anonymize user ID
            anonymized_id = self._anonymize_user_id(user_id)
            
            behavior_entry = {
                "timestamp": datetime.now().isoformat(),
                "anonymized_user_id": anonymized_id,
                "action": action,
                "persona": persona.value,
                "response_time_ms": round(response_time * 1000, 2),
                "metadata": self._sanitize_metadata(metadata or {}),
                "session_hash": self._generate_session_hash(user_id)
            }
            
            self.behavior_data.append(behavior_entry)
            
            # In production, send to analytics service (e.g., Google Analytics, Mixpanel)
            print(f"BEHAVIOR TRACKING: {json.dumps(behavior_entry)}")
            
            return True
        except Exception as e:
            print(f"Behavior tracking error: {e}")
            return False
    
    async def track_persona_interaction(
        self,
        user_id: str,
        persona: PersonaType,
        interaction_type: str,
        success: bool,
        details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Track how users interact with different persona interfaces"""
        try:
            anonymized_id = self._anonymize_user_id(user_id)
            
            interaction_entry = {
                "timestamp": datetime.now().isoformat(),
                "anonymized_user_id": anonymized_id,
                "persona": persona.value,
                "interaction_type": interaction_type,
                "success": success,
                "details": self._sanitize_metadata(details or {}),
                "event_type": "persona_interaction"
            }
            
            self.behavior_data.append(interaction_entry)
            return True
        except Exception as e:
            print(f"Persona interaction tracking error: {e}")
            return False
    
    async def track_content_engagement(
        self,
        user_id: str,
        content_type: str,
        engagement_time: float,
        persona: PersonaType,
        content_id: Optional[str] = None
    ) -> bool:
        """Track how long users engage with different content types"""
        try:
            anonymized_id = self._anonymize_user_id(user_id)
            
            engagement_entry = {
                "timestamp": datetime.now().isoformat(),
                "anonymized_user_id": anonymized_id,
                "content_type": content_type,
                "engagement_time_ms": round(engagement_time * 1000, 2),
                "persona": persona.value,
                "content_id": content_id,
                "event_type": "content_engagement"
            }
            
            self.behavior_data.append(engagement_entry)
            return True
        except Exception as e:
            print(f"Content engagement tracking error: {e}")
            return False
    
    async def get_persona_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get analytics about persona usage and effectiveness"""
        try:
            recent_data = self._get_recent_behavior_data(days)
            
            # Persona distribution
            persona_counts = {}
            response_times_by_persona = {}
            success_rates_by_persona = {}
            
            for entry in recent_data:
                persona = entry.get("persona")
                if persona:
                    persona_counts[persona] = persona_counts.get(persona, 0) + 1
                    
                    # Track response times
                    if "response_time_ms" in entry:
                        if persona not in response_times_by_persona:
                            response_times_by_persona[persona] = []
                        response_times_by_persona[persona].append(entry["response_time_ms"])
                    
                    # Track success rates for interactions
                    if entry.get("event_type") == "persona_interaction":
                        if persona not in success_rates_by_persona:
                            success_rates_by_persona[persona] = {"total": 0, "success": 0}
                        success_rates_by_persona[persona]["total"] += 1
                        if entry.get("success"):
                            success_rates_by_persona[persona]["success"] += 1
            
            # Calculate averages
            avg_response_times = {}
            for persona, times in response_times_by_persona.items():
                avg_response_times[persona] = round(sum(times) / len(times), 2) if times else 0
            
            success_percentages = {}
            for persona, data in success_rates_by_persona.items():
                success_percentages[persona] = round(
                    (data["success"] / data["total"] * 100) if data["total"] > 0 else 0, 2
                )
            
            return {
                "period_days": days,
                "total_interactions": len(recent_data),
                "persona_distribution": persona_counts,
                "avg_response_times_ms": avg_response_times,
                "success_rates_percent": success_percentages,
                "most_popular_persona": max(persona_counts, key=persona_counts.get) if persona_counts else None
            }
        except Exception as e:
            print(f"Analytics error: {e}")
            return {}
    
    def _anonymize_user_id(self, user_id: str) -> str:
        """Create anonymized hash of user ID"""
        # Use SHA-256 hash with salt for anonymization
        salt = "healthlens_behavior_salt_2024"
        return hashlib.sha256(f"{user_id}{salt}".encode()).hexdigest()[:16]
    
    def _generate_session_hash(self, user_id: str) -> str:
        """Generate session hash for behavior tracking"""
        hour = datetime.now().strftime("%Y%m%d%H")
        return hashlib.md5(f"{user_id}_{hour}".encode()).hexdigest()[:8]
    
    def _sanitize_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Remove personally identifiable information from metadata"""
        sanitized = {}
        
        # Allowed metadata fields (non-PII)
        allowed_fields = [
            "action_type", "persona", "lab_results_count", "abnormal_count",
            "response_time", "cache_hit", "error_type", "feature_used",
            "ui_component", "content_type"
        ]
        
        for key, value in metadata.items():
            if key in allowed_fields:
                sanitized[key] = value
        
        return sanitized
    
    def _get_recent_behavior_data(self, days: int) -> list:
        """Get behavior data from the last N days"""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days)
        
        return [
            entry for entry in self.behavior_data 
            if datetime.fromisoformat(entry["timestamp"]) > cutoff
        ]