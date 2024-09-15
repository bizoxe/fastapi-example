"""add new columns

Revision ID: 772862634e71
Revises: f59b89674ea2
Create Date: 2024-09-05 19:30:14.442232

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "772862634e71"
down_revision: Union[str, None] = "f59b89674ea2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(None, "posts", "users", ["user_id"], ["id"])


def downgrade() -> None:
    op.drop_constraint(None, "posts", type_="foreignkey")
    op.drop_column("posts", "user_id")
