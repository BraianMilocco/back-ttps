"""agregar relacion user_espacio_obligado

Revision ID: c3a1fca81eb6
Revises: 72c93d4a7328
Create Date: 2023-09-19 21:32:59.358585

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3a1fca81eb6'
down_revision: Union[str, None] = '72c93d4a7328'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_espacio_association',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('espacio_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['espacio_id'], ['espacios_obligados.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_espacio_association')
    # ### end Alembic commands ###
