"""empty message

Revision ID: 404a2745197b
Revises: f05241d33ac4
Create Date: 2019-11-25 13:12:57.397016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '404a2745197b'
down_revision = 'f05241d33ac4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tickets', sa.Column('event_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tickets', 'events', ['event_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tickets', type_='foreignkey')
    op.drop_column('tickets', 'event_id')
    # ### end Alembic commands ###
