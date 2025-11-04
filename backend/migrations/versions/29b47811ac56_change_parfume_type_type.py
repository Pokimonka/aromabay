"""Change parfume_type type

Revision ID: 29b47811ac56
Revises: 
Create Date: 2025-10-03 00:00:27.021720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from app.models import PerfumeType

# revision identifiers, used by Alembic.
revision: str = '29b47811ac56'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

#'FLORAL', 'WOODY', 'ORIENTAL', 'FRESH', 'CITRUS'
def upgrade() -> None:
    perfume_type_enum = postgresql.ENUM(
        'FLORAL', 'WOODY', 'ORIENTAL', 'FRESH', 'CITRUS', 'GOURMAND', 'AQUATIC', 'CHYPRE', 'FOUGERE',
        name='perfumetype'
    )
    perfume_type_enum.create(op.get_bind())
    # Преобразуем данные из старого типа в новый

    op.alter_column('perfumes', 'perfume_type',
                    type_=perfume_type_enum,
                    postgresql_using="UPPER(perfume_type)::perfumetype",
                    nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    op.alter_column('perfumes', 'perfume_type',
                    type_=sa.String(20),
                    postgresql_using="perfume_type::text",
                    nullable=False)

    # Удаляем Enum тип
    op.execute('DROP TYPE perfumetype')
    # ### end Alembic commands ###
