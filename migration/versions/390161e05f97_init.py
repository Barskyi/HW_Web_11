"""Init

Revision ID: 390161e05f97
Revises: 95446bdd33d3
Create Date: 2024-01-14 15:02:55.979741

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '390161e05f97'
down_revision: Union[str, None] = '95446bdd33d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contacts', 'number', type_=sa.String(length=20))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contacts', 'number', type_=sa.Integer())

    # ### end Alembic commands ###
