from db.repositories import UserRepository
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Depends
from services.auth_service import AuthService

router = APIRouter(prefix="/v1")

@router.get("/me")
async def me(user_id: str = Depends(AuthService.verify_token)):
    user_repo = UserRepository()
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return JSONResponse(
        status_code=200,
        content={
            "name": user["name"],
            "last_name": user["last_name"],
            "username": f'{user["name"]} {user["last_name"]}'.title(),
            "cpf": user["cpf"],
            "email": user.get("email", ""),
            "is_admin": user.get("is_admin", False),
        },
    )
