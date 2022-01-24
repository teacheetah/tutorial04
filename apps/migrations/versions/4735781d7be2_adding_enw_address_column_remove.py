"""adding enw address column remove

Revision ID: 4735781d7be2
Revises: a45788bf0287
Create Date: 2022-01-24 01:05:07.543133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4735781d7be2'
down_revision = 'a45788bf0287'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('auths', 'address')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('auths', sa.Column('address', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    # ### end Alembic commands ###