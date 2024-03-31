"""empty message

Revision ID: f3b26d6bd083
Revises: 
Create Date: 2024-03-31 16:18:20.513377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3b26d6bd083'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('service',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=128), nullable=False),
    sa.Column('price', sa.DECIMAL(scale=2), nullable=False),
    sa.Column('title', sa.VARCHAR(length=256), nullable=False),
    sa.CheckConstraint('price > 0'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('email', sa.VARCHAR(length=128), nullable=False),
    sa.Column('password', sa.CHAR(length=60), nullable=False),
    sa.Column('is_admin', sa.BOOLEAN(), nullable=True),
    sa.CheckConstraint("email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z]{2,}$'"),
    sa.CheckConstraint('length(email) >=5'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('entry',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=False),
    sa.Column('service_id', sa.BIGINT(), nullable=True),
    sa.Column('entry_time', sa.DATETIME(), nullable=False),
    sa.CheckConstraint('entry_time >= datetime.now()'),
    sa.ForeignKeyConstraint(['service_id'], ['service.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('entry_time')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entry')
    op.drop_table('user')
    op.drop_table('service')
    # ### end Alembic commands ###
