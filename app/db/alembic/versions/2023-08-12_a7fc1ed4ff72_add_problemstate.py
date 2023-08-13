"""Add ProblemState

Revision ID: a7fc1ed4ff72
Revises: 0bb66f89cdcb
Create Date: 2023-08-12 16:16:03.158828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7fc1ed4ff72'
down_revision = '0bb66f89cdcb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('problem_states',
    sa.Column('training_session_id', sa.UUID(), nullable=False),
    sa.Column('problem_alias', sa.String(length=255), nullable=False),
    sa.Column('status', sa.Enum('NOT_SUBMITTED', 'PASSED', 'FAILED', name='problemstatusenum'), nullable=False),
    sa.Column('attempts', sa.Integer(), nullable=False),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('dt_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('dt_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['training_session_id'], ['training_sessions.id'], name=op.f('fk__problem_states__training_session_id__training_sessions')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__problem_states')),
    sa.UniqueConstraint('id', name=op.f('uq__problem_states__id'))
    )


def downgrade() -> None:
    op.drop_table('problem_states')
    sa.Enum('NOT_SUBMITTED', 'PASSED', 'FAILED', name='problemstatusenum').drop(op.get_bind())
