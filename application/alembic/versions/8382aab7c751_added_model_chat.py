"""added model chat

Revision ID: 8382aab7c751
Revises: f16189733fec
Create Date: 2026-11-08 15:59:16.471496

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "8382aab7c751"
down_revision: Union[str, Sequence[str], None] = "f16189733fec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "chats",
        sa.Column("create_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "chat_participants",
        sa.Column("chat_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["chat_id"],
            ["chats.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "messages", sa.Column("chat_id", sa.Integer(), nullable=False)
    )
    op.drop_constraint(
        op.f("messages_receiver_id_fkey"), "messages", type_="foreignkey"
    )
    op.create_foreign_key(None, "messages", "chats", ["chat_id"], ["id"])
    op.drop_column("messages", "receiver_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "messages",
        sa.Column(
            "receiver_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
    )
    op.drop_constraint(None, "messages", type_="foreignkey")
    op.create_foreign_key(
        op.f("messages_receiver_id_fkey"),
        "messages",
        "users",
        ["receiver_id"],
        ["id"],
    )
    op.drop_column("messages", "chat_id")
    op.drop_table("chat_participants")
    op.drop_table("chats")
    # ### end Alembic commands ###
