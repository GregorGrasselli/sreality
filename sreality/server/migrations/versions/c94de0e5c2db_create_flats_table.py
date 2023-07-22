"""Create flats table

Revision ID: c94de0e5c2db
Revises: 
Create Date: 2023-07-22 12:01:18.760699

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c94de0e5c2db"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "flats",
        sa.Column("flat_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("image_url", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("flat_id"),
    )


def downgrade():
    op.drop_table("flat")
