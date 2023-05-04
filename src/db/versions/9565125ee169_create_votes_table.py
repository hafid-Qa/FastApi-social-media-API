"""create votes table

Revision ID: 9565125ee169
Revises: 781b94656358
Create Date: 2023-01-27 22:15:37.245762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9565125ee169"
down_revision = "781b94656358"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "votes",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "post_id"),
    )
    pass


def downgrade() -> None:
    op.drop_table("votes")
    pass
