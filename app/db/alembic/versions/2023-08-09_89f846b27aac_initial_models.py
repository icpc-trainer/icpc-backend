"""Initial models

Revision ID: 89f846b27aac
Revises: 
Create Date: 2023-08-09 13:38:40.179301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89f846b27aac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('contests',
    sa.Column('external_id', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('dt_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('dt_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__contests')),
    sa.UniqueConstraint('external_id', name=op.f('uq__contests__external_id')),
    sa.UniqueConstraint('id', name=op.f('uq__contests__id'))
    )
    op.create_table('teams',
    sa.Column('external_id', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('dt_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('dt_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__teams')),
    sa.UniqueConstraint('external_id', name=op.f('uq__teams__external_id')),
    sa.UniqueConstraint('id', name=op.f('uq__teams__id'))
    )
    op.create_table('users',
    sa.Column('external_id', sa.String(length=255), nullable=False),
    sa.Column('login', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('dt_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('dt_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__users')),
    sa.UniqueConstraint('external_id', name=op.f('uq__users__external_id')),
    sa.UniqueConstraint('id', name=op.f('uq__users__id')),
    sa.UniqueConstraint('login', name=op.f('uq__users__login'))
    )
    op.create_table('problems',
    sa.Column('external_id', sa.String(length=255), nullable=False),
    sa.Column('contest_id', sa.UUID(), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=False),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('dt_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('dt_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['contest_id'], ['contests.id'], name=op.f('fk__problems__contest_id__contests')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__problems')),
    sa.UniqueConstraint('external_id', name=op.f('uq__problems__external_id')),
    sa.UniqueConstraint('id', name=op.f('uq__problems__id'))
    )
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
    op.create_table('user_teams',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('team_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], name=op.f('fk__user_teams__team_id__teams'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk__user_teams__user_id__users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'team_id', name=op.f('pk__user_teams'))
    )
    op.create_table('comments',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('problem_id', sa.UUID(), nullable=False),
    sa.Column('training_session_id', sa.UUID(), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=False),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('dt_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('dt_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], name=op.f('fk__comments__problem_id__problems')),
    sa.ForeignKeyConstraint(['training_session_id'], ['training_sessions.id'], name=op.f('fk__comments__training_session_id__training_sessions')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk__comments__user_id__users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__comments')),
    sa.UniqueConstraint('id', name=op.f('uq__comments__id'))
    )
    op.create_table('submissions',
    sa.Column('problem_id', sa.UUID(), nullable=False),
    sa.Column('training_session_id', sa.UUID(), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=False),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('dt_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('dt_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], name=op.f('fk__submissions__problem_id__problems')),
    sa.ForeignKeyConstraint(['training_session_id'], ['training_sessions.id'], name=op.f('fk__submissions__training_session_id__training_sessions')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__submissions')),
    sa.UniqueConstraint('id', name=op.f('uq__submissions__id'))
    )


def downgrade() -> None:
    op.drop_table('submissions')
    op.drop_table('comments')
    op.drop_table('user_teams')
    op.drop_table('training_sessions')
    sa.Enum('IN_PROCESS', 'FINISHED', name='trainingstatusenum').drop(op.get_bind())
    op.drop_table('problems')
    op.drop_table('users')
    op.drop_table('teams')
    op.drop_table('contests')
