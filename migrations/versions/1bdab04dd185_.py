"""empty message

Revision ID: 1bdab04dd185
Revises: 2e4f9fc369d4
Create Date: 2022-05-26 19:46:07.327360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1bdab04dd185'
down_revision = '2e4f9fc369d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todolists', sa.Column('selected', sa.Boolean(), nullable=True))
    op.drop_column('todolists', 'select')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todolists', sa.Column('select', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('todolists', 'selected')
    # ### end Alembic commands ###
