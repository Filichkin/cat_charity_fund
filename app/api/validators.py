from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.core.config import Messages
from app.models import CharityProject


async def get_project_or_404(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=Messages.PROJECT_NOT_FOUND
        )
    return charity_project


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession
) -> None:
    if await charity_project_crud.get_by_attribute(
        'name', project_name, session
    ) is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=Messages.PROJECT_NAME_OCCUPIED
        )


async def check_charity_project_before_delete(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    charity_project = await get_project_or_404(project_id, session)
    if charity_project.invested_amount > 0 or charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=Messages.PROJECT_INVESTED
        )
    return charity_project