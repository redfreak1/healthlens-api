from fastapi import APIRouter, HTTPException
from app.models.schemas import UserProfile, LabResult
from app.services.data_service import DataService
from typing import List

router = APIRouter()
data_service = DataService()

@router.get("/profile/{user_id}", response_model=UserProfile)
async def get_user_profile(user_id: str):
    """Get user profile by ID"""
    try:
        return await data_service.get_user_profile(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/lab-results/{user_id}", response_model=List[LabResult])
async def get_lab_results(user_id: str, report_id: str = None):
    """Get lab results for user"""
    try:
        return await data_service.get_lab_results(user_id, report_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/lab-results/{user_id}/abnormal", response_model=List[LabResult])
async def get_abnormal_results(user_id: str):
    """Get only abnormal lab results for user"""
    try:
        return await data_service.get_abnormal_results(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{user_id}")
async def get_user_history(user_id: str):
    """Get user health history"""
    try:
        return await data_service.get_user_history(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/profile", response_model=UserProfile)
async def create_user_profile(profile_data: dict):
    """Create new user profile"""
    try:
        return await data_service.create_user_profile(profile_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))