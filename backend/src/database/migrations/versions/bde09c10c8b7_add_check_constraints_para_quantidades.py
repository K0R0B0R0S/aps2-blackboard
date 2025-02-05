"""add check constraints para quantidades

Revision ID: bde09c10c8b7
Revises: 6e27bea3d57a
Create Date: 2025-02-05 15:45:55.119040

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bde09c10c8b7'
down_revision: Union[str, None] = '6e27bea3d57a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Adiciona a restrição de verificação para a tabela 'item_compra'
    op.create_check_constraint(
        'chk_quantidade_positiva_item_compra',
        'item_compra',
        'quantidade >= 0'
    )

    # Adiciona a restrição de verificação para a tabela 'item_venda'
    op.create_check_constraint(
        'chk_quantidade_positiva_item_venda',
        'item_venda',
        'quantidade >= 0'
    )

def downgrade():
    # Remove a restrição de verificação da tabela 'item_compra'
    op.drop_constraint(
        'chk_quantidade_positiva_item_compra',
        'item_compra',
        type_='check'
    )

    # Remove a restrição de verificação da tabela 'item_venda'
    op.drop_constraint(
        'chk_quantidade_positiva_item_venda',
        'item_venda',
        type_='check'
    )