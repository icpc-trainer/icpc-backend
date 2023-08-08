"""Rename contest_trainings to training_sessions

Revision ID: f1fe482b08b8
Revises: 937734c5250b
Create Date: 2023-08-09 00:39:50.042179

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f1fe482b08b8'
down_revision = '937734c5250b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('training_sessions',
    sa.Column('contest_id', sa.UUID(), nullable=False),
    sa.Column('team_id', sa.UUID(), nullable=False),
    sa.Column('status', sa.Enum('IN_PROCESS', 'FINISHED', name='trainingstatusenum'), nullable=False),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('dt_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('dt_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['contest_id'], ['contests.id'], name=op.f('fk__training_sessions__contest_id__contests')),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], name=op.f('fk__training_sessions__team_id__teams')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__training_sessions')),
    sa.UniqueConstraint('id', name=op.f('uq__training_sessions__id'))
    )
    op.drop_table('contest_trainings')
    op.add_column('comments', sa.Column('training_session_id', sa.UUID(), nullable=False))
    op.create_unique_constraint(op.f('uq__comments__id'), 'comments', ['id'])
    op.drop_constraint('fk__comments__contest_training_id__contest_trainings', 'comments', type_='foreignkey')
    op.create_foreign_key(op.f('fk__comments__training_session_id__training_sessions'), 'comments', 'training_sessions', ['training_session_id'], ['id'])
    op.drop_column('comments', 'contest_training_id')
    op.create_unique_constraint(op.f('uq__contests__id'), 'contests', ['id'])
    op.create_unique_constraint(op.f('uq__problems__id'), 'problems', ['id'])
    op.add_column('submissions', sa.Column('training_session_id', sa.UUID(), nullable=False))
    op.create_unique_constraint(op.f('uq__submissions__id'), 'submissions', ['id'])
    op.drop_constraint('fk__submissions__contest_training_id__contest_trainings', 'submissions', type_='foreignkey')
    op.create_foreign_key(op.f('fk__submissions__training_session_id__training_sessions'), 'submissions', 'training_sessions', ['training_session_id'], ['id'])
    op.drop_column('submissions', 'contest_training_id')
    op.create_unique_constraint(op.f('uq__teams__id'), 'teams', ['id'])
    op.create_unique_constraint(op.f('uq__users__id'), 'users', ['id'])


def downgrade() -> None:
    op.drop_constraint(op.f('uq__users__id'), 'users', type_='unique')
    op.drop_constraint(op.f('uq__teams__id'), 'teams', type_='unique')
    op.add_column('submissions', sa.Column('contest_training_id', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(op.f('fk__submissions__training_session_id__training_sessions'), 'submissions', type_='foreignkey')
    op.create_foreign_key('fk__submissions__contest_training_id__contest_trainings', 'submissions', 'contest_trainings', ['contest_training_id'], ['id'])
    op.drop_constraint(op.f('uq__submissions__id'), 'submissions', type_='unique')
    op.drop_column('submissions', 'training_session_id')
    op.drop_constraint(op.f('uq__problems__id'), 'problems', type_='unique')
    op.drop_constraint(op.f('uq__contests__id'), 'contests', type_='unique')
    op.add_column('comments', sa.Column('contest_training_id', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(op.f('fk__comments__training_session_id__training_sessions'), 'comments', type_='foreignkey')
    op.create_foreign_key('fk__comments__contest_training_id__contest_trainings', 'comments', 'contest_trainings', ['contest_training_id'], ['id'])
    op.drop_constraint(op.f('uq__comments__id'), 'comments', type_='unique')
    op.drop_column('comments', 'training_session_id')
    op.create_table('contest_trainings',
    sa.Column('contest_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('team_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('status', postgresql.ENUM('IN_PROCESS', 'FINISHED', name='trainingstatusenum'), autoincrement=False, nullable=False),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('dt_created', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=False),
    sa.Column('dt_updated', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['contest_id'], ['contests.id'], name='fk__contest_trainings__contest_id__contests'),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], name='fk__contest_trainings__team_id__teams'),
    sa.PrimaryKeyConstraint('id', name='pk__contest_trainings')
    )
    op.drop_table('training_sessions')
