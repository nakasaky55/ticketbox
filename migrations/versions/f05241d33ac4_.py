"""empty message

Revision ID: f05241d33ac4
Revises: 
Create Date: 2019-11-24 14:26:30.343076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f05241d33ac4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('events_tickets')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events_tickets',
    sa.Column('event_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('ticket_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], name='events_tickets_event_id_fkey'),
    sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], name='events_tickets_ticket_id_fkey'),
    sa.PrimaryKeyConstraint('event_id', 'ticket_id', name='events_tickets_pkey')
    )
    # ### end Alembic commands ###
