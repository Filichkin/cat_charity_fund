from datetime import datetime
from typing import Optional, Type, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.validators import (
    check_charity_project_name_duplicate,
    check_charity_project_invested,
    check_charity_project_is_open,
    check_new_full_amount
)
from app.crud.charityproject import charity_project_crud
from app.models import BaseInvestModel, CharityProject, Donation, User
from app.schemas.charityproject import CharityProjectDB, CharityProjectUpdate


class InvestmentHandler:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    async def close_entity(obj: BaseInvestModel) -> BaseInvestModel:
        obj.invested_amount = obj.full_amount
        obj.fully_invested = True
        obj.close_date = datetime.now()
        return obj

    async def distribute(
            self,
            recipient: BaseInvestModel,
            source: BaseInvestModel
    ) -> tuple[BaseInvestModel, BaseInvestModel]:
        donation_recipient = recipient.full_amount - recipient.invested_amount
        donation_source = source.full_amount - source.invested_amount

        if donation_recipient > donation_source:
            recipient.invested_amount += donation_source
            source = await self.close_entity(source)
        elif donation_recipient == donation_source:
            recipient = await self.close_entity(recipient)
            source = await self.close_entity(source)
        else:
            source.invested_amount += donation_recipient
            recipient = await self.close_entity(recipient)

        return recipient, source

    async def perform_investment(
            self,
            obj_in: BaseInvestModel,
            model_db: Type[Union[Donation, CharityProject]]
    ) -> BaseInvestModel:
        result = await self.session.execute(
            select(model_db).where(
                model_db.fully_invested.is_(False)
            ).order_by(model_db.create_date)
        )
        sources = result.scalars().all()

        for source in sources:
            obj_in, source = await self.distribute(obj_in, source)
            if obj_in.fully_invested:
                break

        await self.session.flush()
        return obj_in


class InvestmentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.handler = InvestmentHandler(session)

    async def create_object(
            self,
            obj_in,
            model,
            user: Optional[User] = None,
            need_for_commit: bool = True
    ) -> BaseInvestModel:
        obj_data = obj_in.dict()

        if 'name' in obj_data:
            await check_charity_project_name_duplicate(
                obj_data['name'], self.session
            )

        if user is not None:
            obj_data['user_id'] = user.id

        db_obj = model(**obj_data)

        self.session.add(db_obj)
        await self.session.flush()

        model_in = Donation if model is CharityProject else CharityProject
        await self.handler.perform_investment(db_obj, model_in)

        if need_for_commit:
            await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update_charity_project(
            self,
            charity_project: CharityProject,
            obj_in: CharityProjectUpdate
    ) -> CharityProjectDB:
        await check_charity_project_is_open(charity_project)

        if obj_in.full_amount is not None:
            check_new_full_amount(
                charity_project.invested_amount,
                obj_in.full_amount
            )

        if obj_in.name:
            await check_charity_project_name_duplicate(
                obj_in.name, self.session
            )

        if (obj_in.full_amount is not None and
                obj_in.full_amount == charity_project.invested_amount):
            charity_project.fully_invested = True
            charity_project.close_date = datetime.now()

        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(charity_project, field, value)

        return await charity_project_crud.update(charity_project, self.session)

    async def remove_charity_project(
            self,
            charity_project: CharityProject,
    ) -> CharityProjectDB:
        await check_charity_project_is_open(charity_project)
        await check_charity_project_invested(charity_project)
        return await charity_project_crud.remove(charity_project, self.session)