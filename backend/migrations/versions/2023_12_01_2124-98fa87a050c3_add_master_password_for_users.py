"""add master password for users

Revision ID: 98fa87a050c3
Revises: a0007628d1a0
Create Date: 2023-12-01 21:24:31.425296

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "98fa87a050c3"
down_revision: Union[str, None] = "a0007628d1a0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "master_password",
            sa.LargeBinary(),
            server_default="4536736c567a6b5544754256787a63746c7932624e6e464d74307147476b346744424c394238357a6a42673d",
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "master_password")
    # ### end Alembic commands ###
