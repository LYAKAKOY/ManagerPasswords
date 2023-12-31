from typing import List

from api.actions.auth import get_current_user_from_token
from api.actions.passwords import _create_or_update_password
from api.actions.passwords import _delete_password_by_service_name
from api.actions.passwords import _get_all_passwords
from api.actions.passwords import _get_password_by_service_name
from api.actions.passwords import _get_passwords_by_match_service_name
from api.passwords.schemas import CreatePassword
from api.passwords.schemas import DeletedPassword
from api.passwords.schemas import ShowPassword
from db.session import get_db
from db.users.models import User
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

manager_passwords_router = APIRouter()


@manager_passwords_router.post("/{service_name}", response_model=ShowPassword)
async def create_or_update_password(
    service_name: str,
    password: CreatePassword,
    current_user: User = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db),
) -> ShowPassword:
    """Create or update password of service"""
    service_password = await _create_or_update_password(
        service_name, password, current_user, db
    )
    if service_password is None:
        raise HTTPException(status_code=500, detail="An error occurred try again")
    return service_password


@manager_passwords_router.get("/by_match", response_model=List[ShowPassword])
async def get_passwords_by_match(
    match_service_name: str,
    current_user: User = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db),
) -> List[ShowPassword]:
    """Get password(s) by match service name"""
    service_passwords = await _get_passwords_by_match_service_name(
        service_name=match_service_name, user=current_user, session=db
    )
    if not service_passwords:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No service found"
        )
    return service_passwords


@manager_passwords_router.get("/{service_name}", response_model=ShowPassword)
async def get_password(
    service_name: str,
    current_user: User = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db),
) -> ShowPassword:
    """Get password of the service"""
    password = await _get_password_by_service_name(service_name, current_user, db)
    if password is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The password of the service not found",
        )
    return password


@manager_passwords_router.get("/", response_model=List[ShowPassword])
async def get_all_passwords(
    current_user: User = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db),
) -> List[ShowPassword]:
    """Get all passwords"""
    service_passwords = await _get_all_passwords(user=current_user, session=db)
    if not service_passwords:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not a single password was found",
        )
    return service_passwords


@manager_passwords_router.delete("/{service_name}", response_model=DeletedPassword)
async def delete_password_by_service_name(
    service_name: str,
    current_user: User = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db),
) -> DeletedPassword:
    """Delete password by service name"""
    deleted_password = await _delete_password_by_service_name(
        service_name=service_name, user=current_user, session=db
    )
    if not deleted_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="service not found"
        )
    return deleted_password
