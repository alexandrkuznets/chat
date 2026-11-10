"""added unique constraint for chatpaticipant

Revision ID: f78b539b7c47
Revises: 8382aab7c751
Create Date: 2026-11-10 20:08:07.681276

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "f78b539b7c47"
down_revision: Union[str, Sequence[str], None] = "8382aab7c751"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        "uq_chat_user", "chat_participants", ["chat_id", "user_id"]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_chat_user", "chat_participants", type_="unique")
    # ### end Alembic commands ###
