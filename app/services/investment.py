from datetime import datetime

from app.models.base import BaseInvestModel


def investment(
    target: BaseInvestModel,
    sources: list[BaseInvestModel]
) -> list[BaseInvestModel]:
    modified = []
    for source in sources:
        invest_amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        for obj in source, target:
            obj.invested_amount += invest_amount
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()
        modified.append(source)
        if target.fully_invested:
            break
    return modified