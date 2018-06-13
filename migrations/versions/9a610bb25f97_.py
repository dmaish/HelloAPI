"""empty message

Revision ID: 9a610bb25f97
Revises: 7328f4eded60
Create Date: 2018-05-19 13:27:15.681410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a610bb25f97'
down_revision = '7328f4eded60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('borrow_records', 'time_borrowed',
               existing_type=sa.VARCHAR(length=60),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('borrow_records', 'time_borrowed',
               existing_type=sa.VARCHAR(length=60),
               nullable=True)
    # ### end Alembic commands ###