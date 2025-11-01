from app.models.schemas import UserProfile, LabResult, LabResultStatus
from typing import List, Optional, Dict, Any
import json
from datetime import datetime

class DataService:
    def __init__(self):
        # In a real implementation, this would connect to a database
        self.mock_data = self._load_mock_data()
    
    def _load_mock_data(self):
        """Load mock data similar to the React app's mockLabData"""
        return {
            "users": {
                "123": {
                    "id": "123",
                    "age": 72,
                    "gender": "Female",
                    "conditions": "Type 2 Diabetes, Hypertension",
                    "created_at": "2024-01-15T10:30:00Z"
                },
                "456": {
                    "id": "456",
                    "age": 45,
                    "gender": "Male",
                    "conditions": None,
                    "created_at": "2024-02-20T14:15:00Z"
                }
            },
            "lab_results": {
                "123": [
                    {
                        "name": "Glucose",
                        "value": 98.0,
                        "unit": "mg/dL",
                        "reference_range": {"min": 70.0, "max": 99.0},
                        "category": "Metabolic Panel",
                        "status": "normal"
                    },
                    {
                        "name": "White Blood Cell Count",
                        "value": 11.2,
                        "unit": "K/uL",
                        "reference_range": {"min": 4.5, "max": 11.0},
                        "category": "Complete Blood Count",
                        "status": "high"
                    },
                    {
                        "name": "Red Blood Cell Count",
                        "value": 4.8,
                        "unit": "M/uL",
                        "reference_range": {"min": 4.5, "max": 5.9},
                        "category": "Complete Blood Count",
                        "status": "normal"
                    },
                    {
                        "name": "Hemoglobin",
                        "value": 14.2,
                        "unit": "g/dL",
                        "reference_range": {"min": 13.5, "max": 17.5},
                        "category": "Complete Blood Count",
                        "status": "normal"
                    },
                    {
                        "name": "Hematocrit",
                        "value": 42.1,
                        "unit": "%",
                        "reference_range": {"min": 38.8, "max": 50.0},
                        "category": "Complete Blood Count",
                        "status": "normal"
                    },
                    {
                        "name": "Platelet Count",
                        "value": 210.0,
                        "unit": "K/uL",
                        "reference_range": {"min": 150.0, "max": 400.0},
                        "category": "Complete Blood Count",
                        "status": "normal"
                    },
                    {
                        "name": "Sodium",
                        "value": 138.0,
                        "unit": "mmol/L",
                        "reference_range": {"min": 136.0, "max": 145.0},
                        "category": "Metabolic Panel",
                        "status": "normal"
                    },
                    {
                        "name": "Potassium",
                        "value": 3.2,
                        "unit": "mmol/L",
                        "reference_range": {"min": 3.5, "max": 5.1},
                        "category": "Metabolic Panel",
                        "status": "low"
                    },
                    {
                        "name": "Creatinine",
                        "value": 1.0,
                        "unit": "mg/dL",
                        "reference_range": {"min": 0.7, "max": 1.3},
                        "category": "Metabolic Panel",
                        "status": "normal"
                    },
                    {
                        "name": "Total Cholesterol",
                        "value": 195.0,
                        "unit": "mg/dL",
                        "reference_range": {"min": 0.0, "max": 200.0},
                        "category": "Lipid Panel",
                        "status": "normal"
                    }
                ]
            },
            "user_history": {
                "123": {
                    "previous_conditions": ["Pre-diabetes", "High cholesterol"],
                    "medications": ["Metformin", "Lisinopril"],
                    "lifestyle_factors": ["Active", "Watches diet"],
                    "family_history": ["Diabetes", "Heart disease"],
                    "last_visit": "2024-10-15T09:00:00Z"
                }
            }
        }
    
    async def get_user_profile(self, user_id: str) -> UserProfile:
        """Fetch user profile by ID"""
        user_data = self.mock_data["users"].get(user_id)
        if not user_data:
            raise ValueError(f"User {user_id} not found")
        
        return UserProfile(**user_data)
    
    async def get_lab_results(self, user_id: str, report_id: Optional[str] = None) -> List[LabResult]:
        """Fetch lab results for user"""
        lab_data = self.mock_data["lab_results"].get(user_id, [])
        
        # Convert to LabResult objects
        results = []
        for result in lab_data:
            results.append(LabResult(**result))
        
        return results
    
    async def get_user_history(self, user_id: str) -> Dict[str, Any]:
        """Fetch user health history"""
        return self.mock_data["user_history"].get(user_id, {})
    
    async def create_user_profile(self, profile_data: Dict[str, Any]) -> UserProfile:
        """Create new user profile"""
        user_id = str(len(self.mock_data["users"]) + 1)
        profile_data["id"] = user_id
        profile_data["created_at"] = datetime.now().isoformat()
        
        self.mock_data["users"][user_id] = profile_data
        return UserProfile(**profile_data)
    
    async def update_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> UserProfile:
        """Update existing user profile"""
        if user_id not in self.mock_data["users"]:
            raise ValueError(f"User {user_id} not found")
        
        self.mock_data["users"][user_id].update(profile_data)
        return UserProfile(**self.mock_data["users"][user_id])
    
    async def store_lab_results(self, user_id: str, lab_results: List[Dict[str, Any]]) -> bool:
        """Store lab results for user"""
        self.mock_data["lab_results"][user_id] = lab_results
        return True
    
    async def get_abnormal_results(self, user_id: str) -> List[LabResult]:
        """Get only abnormal lab results for user"""
        all_results = await self.get_lab_results(user_id)
        return [result for result in all_results if result.status != LabResultStatus.NORMAL]