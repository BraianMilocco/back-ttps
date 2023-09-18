"""Agregar modelo sede y responsable_sede

Revision ID: a1a185e2dc1b
Revises: 06b9b33a3264
Create Date: 2023-09-17 22:13:05.346146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1a185e2dc1b'
down_revision: Union[str, None] = '06b9b33a3264'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sedes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(), nullable=False),
    sa.Column('numero', sa.Integer(), nullable=False),
    sa.Column('sector', sa.String(), nullable=True),
    sa.Column('tipo', sa.String(), nullable=True),
    sa.Column('direccion', sa.String(), nullable=True),
    sa.Column('latitud', sa.String(), nullable=True),
    sa.Column('longitud', sa.String(), nullable=True),
    sa.Column('superficie', sa.Integer(), nullable=True),
    sa.Column('cantidad_pisos', sa.Integer(), nullable=True),
    sa.Column('cantidad_personas_externas', sa.Integer(), nullable=True),
    sa.Column('cantidad_personas_estables', sa.Integer(), nullable=True),
    sa.Column('entidad_id', sa.Integer(), nullable=False),
    sa.Column('provincia_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.CheckConstraint("sector IN ('publico', 'privado')"),
    sa.ForeignKeyConstraint(['entidad_id'], ['entidades.id'], ),
    sa.ForeignKeyConstraint(['provincia_id'], ['provincias.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('numero', 'entidad_id', name='uq_numero_entidad')
    )
    op.create_index(op.f('ix_sedes_cantidad_personas_estables'), 'sedes', ['cantidad_personas_estables'], unique=False)
    op.create_index(op.f('ix_sedes_cantidad_personas_externas'), 'sedes', ['cantidad_personas_externas'], unique=False)
    op.create_index(op.f('ix_sedes_cantidad_pisos'), 'sedes', ['cantidad_pisos'], unique=False)
    op.create_index(op.f('ix_sedes_direccion'), 'sedes', ['direccion'], unique=False)
    op.create_index(op.f('ix_sedes_id'), 'sedes', ['id'], unique=False)
    op.create_index(op.f('ix_sedes_latitud'), 'sedes', ['latitud'], unique=False)
    op.create_index(op.f('ix_sedes_longitud'), 'sedes', ['longitud'], unique=False)
    op.create_index(op.f('ix_sedes_nombre'), 'sedes', ['nombre'], unique=False)
    op.create_index(op.f('ix_sedes_numero'), 'sedes', ['numero'], unique=False)
    op.create_index(op.f('ix_sedes_sector'), 'sedes', ['sector'], unique=False)
    op.create_index(op.f('ix_sedes_superficie'), 'sedes', ['superficie'], unique=False)
    op.create_index(op.f('ix_sedes_tipo'), 'sedes', ['tipo'], unique=False)
    op.create_table('responsables_sedes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(), nullable=True),
    sa.Column('telefono', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('sede_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['sede_id'], ['sedes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_responsables_sedes_email'), 'responsables_sedes', ['email'], unique=False)
    op.create_index(op.f('ix_responsables_sedes_id'), 'responsables_sedes', ['id'], unique=False)
    op.create_index(op.f('ix_responsables_sedes_nombre'), 'responsables_sedes', ['nombre'], unique=False)
    op.create_index(op.f('ix_responsables_sedes_telefono'), 'responsables_sedes', ['telefono'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_responsables_sedes_telefono'), table_name='responsables_sedes')
    op.drop_index(op.f('ix_responsables_sedes_nombre'), table_name='responsables_sedes')
    op.drop_index(op.f('ix_responsables_sedes_id'), table_name='responsables_sedes')
    op.drop_index(op.f('ix_responsables_sedes_email'), table_name='responsables_sedes')
    op.drop_table('responsables_sedes')
    op.drop_index(op.f('ix_sedes_tipo'), table_name='sedes')
    op.drop_index(op.f('ix_sedes_superficie'), table_name='sedes')
    op.drop_index(op.f('ix_sedes_sector'), table_name='sedes')
    op.drop_index(op.f('ix_sedes_numero'), table_name='sedes')
    op.drop_index(op.f('ix_sedes_nombre'), table_name='sedes')
    op.drop_index(op.f('ix_sedes_longitud'), table_name='sedes')
    op.drop_index(op.f('ix_sedes_latitud'), table_name='sedes')
    op.drop_index(op.f('ix_sedes_id'), table_name='sedes')
    op.drop_index(op.f('ix_sedes_direccion'), table_name='sedes')
    op.drop_index(op.f('ix_sedes_cantidad_pisos'), table_name='sedes')
    op.drop_index(op.f('ix_sedes_cantidad_personas_externas'), table_name='sedes')
    op.drop_index(op.f('ix_sedes_cantidad_personas_estables'), table_name='sedes')
    op.drop_table('sedes')
    # ### end Alembic commands ###
