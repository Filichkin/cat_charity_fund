from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import BaseInvestModel


class Donation(BaseInvestModel):
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user'),
        nullable=False
    )
    comment = Column(Text, nullable=True)

    def __repr__(self):
        return (
            f'Donation from User ID: {self.user_id}, '
            f'Comment: {self.comment}, '
            f'{super().__repr__()}'
        )