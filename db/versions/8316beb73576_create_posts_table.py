"""create posts table

Revision ID: 8316beb73576
Revises: 
Create Date: 2023-01-27 21:33:09.021663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8316beb73576"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("published", sa.Boolean(), server_default="True", nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
            onupdate=sa.text("now()"),
        ),
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
