from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db


class BaseController:
    db: AsyncSession

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db


def get_controller(controller):
    def _get_controller(db: AsyncSession = Depends(get_db)) -> BaseController:
        return controller(db)

    return _get_controller
