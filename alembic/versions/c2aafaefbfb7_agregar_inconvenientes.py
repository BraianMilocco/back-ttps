"""agregar inconvenientes

Revision ID: c2aafaefbfb7
Revises: d95dfc782bdb
Create Date: 2023-09-19 21:13:44.943120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2aafaefbfb7'
down_revision: Union[str, None] = 'd95dfc782bdb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('incovenientes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fecha', sa.DateTime(), nullable=True),
    sa.Column('falta_insumos', sa.Boolean(), nullable=True),
    sa.Column('estaba_en_sitio', sa.Boolean(), nullable=True),
    sa.Column('respondio_con_descargas_electricas', sa.Boolean(), nullable=True),
    sa.Column('cantidad_de_descargas', sa.Integer(), nullable=True),
    sa.Column('extra_info', sa.String(), nullable=True),
    sa.Column('muerte_subita_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['muerte_subita_id'], ['muertes_subitas.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('muerte_subita_id')
    )
    op.create_index(op.f('ix_incovenientes_cantidad_de_descargas'), 'incovenientes', ['cantidad_de_descargas'], unique=False)
    op.create_index(op.f('ix_incovenientes_extra_info'), 'incovenientes', ['extra_info'], unique=False)
    op.create_index(op.f('ix_incovenientes_id'), 'incovenientes', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_incovenientes_id'), table_name='incovenientes')
    op.drop_index(op.f('ix_incovenientes_extra_info'), table_name='incovenientes')
    op.drop_index(op.f('ix_incovenientes_cantidad_de_descargas'), table_name='incovenientes')
    op.drop_table('incovenientes')
    # ### end Alembic commands ###
