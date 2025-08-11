from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import Donation, User
from app.schemas.donation import (
    DonationCreate,
    DonationFullDB,
    DonationShortDB
)
from app.services.investment import InvestmentService


router = APIRouter()


@router.post(
    '/',
    response_model=DonationShortDB,
    response_model_exclude_none=True
)
async def create_new_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Only for registered users"""

    invest_object = InvestmentService(session)
    return await invest_object.create_object(
        donation,
        Donation,
        user,
        need_for_commit=False
    )


@router.get(
    '/',
    response_model=list[DonationFullDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Only for superusers"""

    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationShortDB],
    response_model_exclude_none=True,
    response_model_exclude={'user_id'}
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    return await donation_crud.get_by_user(
        session=session,
        user=user
    )