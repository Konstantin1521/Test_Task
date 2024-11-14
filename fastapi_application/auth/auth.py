from fastapi import Depends, APIRouter, Form, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from . import utils_jwt as jwt_auth
from .jwt_schema import TokenInfo

from api.api_v1.crud.crud_user_and_image import CRUDUser
from core.models import db_helper

from api.api_v1.users.user_schema import UserSchema


http_bearer = HTTPBearer()

router = APIRouter(prefix="/auth", tags=["JWT"])


async def validate_user(
    username: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    unauthexception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )
    try:
        user = await CRUDUser.get_element_by_name(
            session=session, element_name=username
        )
    except Exception:
        raise unauthexception
    if not user:
        raise unauthexception
    if not jwt_auth.validate_password(password=password, hashed_password=user.password):
        raise unauthexception
    return user


@router.post("/login", response_model=TokenInfo)
async def login_for_access_token(user: UserSchema = Depends(validate_user)):
    jwt_payload = {
        "sub": user.id,
        "username": user.username,
    }
    token = jwt_auth.encode_jwt(jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")


async def get_current_auth_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    token = credentials.credentials
    payload = jwt_auth.decode_jwt(token)

    user = await CRUDUser.get_element_by_id(session=session, element_id=payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="Token invalid")
    return user
