from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from repositories import UserRepository
from models import LoginRequest
from services.auth_service import AuthService

router = APIRouter(prefix="/v1")

@router.post("/login")
async def login(credentials: LoginRequest):
    auth_service = AuthService()
    user = auth_service.authenticate_user(credentials.email, credentials.password)
    access_token = auth_service.create_access_token(data={"sub": str(user["_id"])})

    return JSONResponse(
        status_code=200,
        content={
            "message": "Login successful",
            "user": {
                "name": user["name"],
                "email": user.get("email", ""),
                "is_admin": user.get("is_admin", False),
                "user_id": str(user["_id"]),
            },
            "token": access_token
        },
    )

# @router.post("/logout")
# async def logout(token: str):
#     session_repo = SessionRepository()
#     session_repo.delete_session(token)

#     return JSONResponse(
#         status_code=200,
#         content={"message": "Logout successful"},
#     )


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
