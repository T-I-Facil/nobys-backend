from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from repositories import HospitalRepository
from models import CreateHospital
from fastapi.encoders import jsonable_encoder
from services import AuthService

router = APIRouter(prefix="/v1")

@router.get("/hospitals")
async def get_hospitals():
    hospital_repo = HospitalRepository()
    hospitals = jsonable_encoder(hospital_repo.get_all())
    return JSONResponse(status_code=200, content=hospitals)

@router.post("/hospitals")
async def create_hospital(hospital: CreateHospital, user_id: str = Depends(AuthService.verify_token)): 
    # if not AuthService.is_admin(user_id):
    #     raise HTTPException(status_code=403, detail="User is not admin")
       
    hospital_repo = HospitalRepository()
    hospital_repo.create(hospital)
    return JSONResponse(status_code=200, content={"message": "Hospital created successfully"})