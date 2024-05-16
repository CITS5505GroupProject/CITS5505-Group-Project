"""added type field to survey

Revision ID: 8f0f5e909322
Revises: e491a9ac966e
Create Date: 2024-05-13 20:05:28.959847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f0f5e909322'
down_revision = 'e491a9ac966e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('survey', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.String(length=50), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('survey', schema=None) as batch_op:
        batch_op.drop_column('type')

    # ### end Alembic commands ###
