"""add phone number to users

Revision ID: 781b94656358
Revises: ec5f390c6902
Create Date: 2023-01-27 22:11:33.116590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "781b94656358"
down_revision = "ec5f390c6902"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column("users","phone_number")
    pass
