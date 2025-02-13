from fastapi import APIRouter
from fastapi.responses import JSONResponse
from repositories import HospitalRepository
from models import CreateHospital
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/v1")

@router.get("/hospitals")
async def get_hospitals():
    hospital_repo = HospitalRepository()
    hospitals = jsonable_encoder(hospital_repo.get_all())
    return JSONResponse(status_code=200, content={"hospitals": hospitals})

@router.post("/hospitals")
async def create_hospital(hospital: CreateHospital):    
    hospital_repo = HospitalRepository()
    hospital_repo.create(hospital)
    return JSONResponse(status_code=200, content={"message": "Hospital created successfully"})