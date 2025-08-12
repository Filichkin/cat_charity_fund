from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from app.core.config import Constants


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=Constants.NAME_MIN_LEN,
        max_length=Constants.NAME_MAX_LEN
    )
    description: Optional[str] = Field(
        None,
        min_length=Constants.NAME_MIN_LEN
    )
    full_amount: Optional[PositiveInt]

    model_config = ConfigDict(extra='forbid')


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        min_length=Constants.NAME_MIN_LEN,
        max_length=Constants.NAME_MAX_LEN
    )
    description: str = Field(
        min_length=Constants.NAME_MIN_LEN
    )
    full_amount: PositiveInt


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=Constants.NAME_MIN_LEN,
        max_length=Constants.NAME_MAX_LEN
    )
    description: Optional[str] = Field(
        None,
        min_length=Constants.NAME_MIN_LEN
    )
    full_amount: Optional[PositiveInt] = None

    model_config = ConfigDict(extra='forbid')


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)