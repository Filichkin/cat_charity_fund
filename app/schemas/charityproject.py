from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator, Field, PositiveInt

from app.core.config import Constants, Messages


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None,
        max_length=Constants.NAME_MAX_LEN,
        min_length=Constants.NAME_MIN_LEN
    )
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt]

    model_config = ConfigDict(extra='forbid')


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        max_length=Constants.NAME_MAX_LEN
    )
    description: str = Field(...)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):

    @field_validator('name')
    def name_cannot_be_none(cls, value: Optional[str]):
        if value is None:
            raise ValueError(Messages.PROJECT_NAME_NOT_NULL)
        return value

    @field_validator('description')
    def description_cannot_be_none(cls, value: Optional[str]):
        if value is None:
            raise ValueError(Messages.PROJECT_DESCRIPTION_NOT_NULL)
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)