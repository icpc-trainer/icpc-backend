"""Add UniqueConstraint to ProblemState

Revision ID: 1eb9c10a63f8
Revises: a7fc1ed4ff72
Create Date: 2023-08-13 12:14:43.500221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1eb9c10a63f8'
down_revision = 'a7fc1ed4ff72'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(op.f('uq__problem_states__training_session_id_problem_alias'), 'problem_states', ['training_session_id', 'problem_alias'])


def downgrade() -> None:
    op.drop_constraint(op.f('uq__problem_states__training_session_id_problem_alias'), 'problem_states', type_='unique')
