"""baseline

Revision ID: 4011aff68caa
Revises:
Create Date: 2026-11-08 16:37:07.442394

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '4011aff68caa'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'applications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company', sa.String(length=100), nullable=False),
        sa.Column('position', sa.String(length=150), nullable=False),
        sa.Column(
            'status',
            sa.String(length=50),
            nullable=False
        ),
        sa.Column('applied_date', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        'ix_applications_id',
        'applications',
        ['id'],
        unique=False
    )


def downgrade() -> None:
    op.drop_index(
        'ix_applications_id',
        table_name='applications'
    )
    op.drop_table('applications')