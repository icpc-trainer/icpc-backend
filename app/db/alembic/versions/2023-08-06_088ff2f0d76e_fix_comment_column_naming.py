"""Fix comment column naming

Revision ID: 088ff2f0d76e
Revises: 711fa326ed72
Create Date: 2023-08-06 16:50:09.034605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '088ff2f0d76e'
down_revision = '711fa326ed72'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('comments', sa.Column('contest_training_id', sa.UUID(), nullable=False))
    op.create_unique_constraint(op.f('uq__comments__id'), 'comments', ['id'])
    op.drop_constraint('fk__comments__status__contest_trainings', 'comments', type_='foreignkey')
    op.create_foreign_key(op.f('fk__comments__contest_training_id__contest_trainings'), 'comments', 'contest_trainings', ['contest_training_id'], ['id'])
    op.drop_column('comments', 'status')
    op.create_unique_constraint(op.f('uq__contest_trainings__id'), 'contest_trainings', ['id'])
    op.create_unique_constraint(op.f('uq__contests__id'), 'contests', ['id'])
    op.create_unique_constraint(op.f('uq__problems__id'), 'problems', ['id'])
    op.create_unique_constraint(op.f('uq__submissions__id'), 'submissions', ['id'])
    op.create_unique_constraint(op.f('uq__teams__id'), 'teams', ['id'])
    op.create_unique_constraint(op.f('uq__users__id'), 'users', ['id'])


def downgrade() -> None:
    op.drop_constraint(op.f('uq__users__id'), 'users', type_='unique')
    op.drop_constraint(op.f('uq__teams__id'), 'teams', type_='unique')
    op.drop_constraint(op.f('uq__submissions__id'), 'submissions', type_='unique')
    op.drop_constraint(op.f('uq__problems__id'), 'problems', type_='unique')
    op.drop_constraint(op.f('uq__contests__id'), 'contests', type_='unique')
    op.drop_constraint(op.f('uq__contest_trainings__id'), 'contest_trainings', type_='unique')
    op.add_column('comments', sa.Column('status', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(op.f('fk__comments__contest_training_id__contest_trainings'), 'comments', type_='foreignkey')
    op.create_foreign_key('fk__comments__status__contest_trainings', 'comments', 'contest_trainings', ['status'], ['id'])
    op.drop_constraint(op.f('uq__comments__id'), 'comments', type_='unique')
    op.drop_column('comments', 'contest_training_id')
