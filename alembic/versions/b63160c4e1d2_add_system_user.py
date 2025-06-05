"""add system user

Revision ID: b63160c4e1d2
Revises: 52bdba5bb348
Create Date: 2025-06-05 15:42:02.263371

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import insert, delete
from app.models.user import User
from sqlalchemy.orm import Session

# revision identifiers, used by Alembic.
revision: str = 'b63160c4e1d2'
down_revision: Union[str, None] = '52bdba5bb348'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        insert(User).values(
            id=0,
            email="system@localhost",
            username="system_bot",
            is_system_user=True,
            hashed_password="password"
        )
    )
    session.commit()


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        delete(User).where(User.id == 0)
    )
    session.commit()
