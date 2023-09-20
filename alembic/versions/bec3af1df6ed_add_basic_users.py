"""Add basic users

Revision ID: bec3af1df6ed
Revises: 4e2ef7a28b05
Create Date: 2023-09-20 15:44:47.110990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bec3af1df6ed"
down_revision: Union[str, None] = "4e2ef7a28b05"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Inserta los usuarios básicos
    op.bulk_insert(
        sa.table(
            "users",
            sa.column("email"),
            sa.column("hashed_password"),
            sa.column("provincia_id"),
            sa.column("rol"),
        ),
        # pass: Pass1234
        # provincias: 1: Buenos Aires, 17: Catamarca
        [
            {
                "email": "representante@mail.com",
                "hashed_password": "$2b$12$htBWJYuDNGDVyEPqiVZYmuOUB8DMoszBzazfFmKITMEKnkH0Lq6eK",
                "provincia_id": None,
                "rol": "representante",
            },
            {
                "email": "provincial@mail.com",
                "hashed_password": "$2b$12$htBWJYuDNGDVyEPqiVZYmuOUB8DMoszBzazfFmKITMEKnkH0Lq6eK",
                "provincia_id": 1,
                "rol": "administrador_provincial",
            },
            {
                "email": "provincial2@mail.com",
                "hashed_password": "$2b$12$htBWJYuDNGDVyEPqiVZYmuOUB8DMoszBzazfFmKITMEKnkH0Lq6eK",
                "provincia_id": 17,
                "rol": "administrador_provincial",
            },
            {
                "email": "certificador@mail.com",
                "hashed_password": "$2b$12$htBWJYuDNGDVyEPqiVZYmuOUB8DMoszBzazfFmKITMEKnkH0Lq6eK",
                "provincia_id": None,
                "rol": "certificador",
            },
        ],
    )


def downgrade() -> None:
    # Elimina los usuarios básicos
    op.execute(
        "DELETE FROM users WHERE email IN ('representante@mail.com', 'provincial@mail.com', 'provincial2@mail.com', 'certificador@mail.com')"
    )
