"""empty message

Revision ID: 3368ac633bb4
Revises: 
Create Date: 2019-10-08 12:52:04.133774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3368ac633bb4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('user_databases',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('drivername', sa.String(length=128), nullable=True),
    sa.Column('username', sa.String(length=128), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('host', sa.String(length=256), nullable=True),
    sa.Column('port', sa.Integer(), nullable=True),
    sa.Column('database', sa.String(length=128), nullable=True),
    sa.Column('query', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_databases')
    op.drop_table('user')
    # ### end Alembic commands ###


def upgrade_user_db():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('calendar_id', sa.String(length=150), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('organizer_email', sa.String(length=200), nullable=True),
    sa.Column('is_recurring', sa.BOOLEAN(), nullable=True),
    sa.Column('title', sa.String(length=500), nullable=True),
    sa.Column('location', sa.String(length=500), nullable=True),
    sa.Column('start_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('end_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('description', sa.String(length=5000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event_attendees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=200), nullable=True),
    sa.Column('working_hours_start_time', sa.TIME(), nullable=True),
    sa.Column('working_hours_end_time', sa.TIME(), nullable=True),
    sa.Column('display_name', sa.String(length=200), nullable=True),
    sa.Column('response_status', sa.String(length=20), nullable=True),
    sa.Column('is_organizer', sa.BOOLEAN(), nullable=True),
    sa.Column('is_optional', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade_user_db():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event_attendees')
    op.drop_table('events')
    # ### end Alembic commands ###
