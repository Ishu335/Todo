from fastapi import APIRouter

router = APIRouter()
@router.get("/auth/")
async def user_auth():
    return  "user authentication"
