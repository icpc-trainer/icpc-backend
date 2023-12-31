"""remove problem table

Revision ID: 0bb66f89cdcb
Revises: 48ad838a0586
Create Date: 2023-08-11 18:28:24.713357

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0bb66f89cdcb'
down_revision = '48ad838a0586'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('comments', sa.Column('problem_alias', sa.String(length=255), nullable=False))
    op.drop_constraint('fk__comments__problem_id__problems', 'comments', type_='foreignkey')
    op.drop_column('comments', 'problem_id')
    op.add_column('submissions', sa.Column('problem_alias', sa.String(length=255), nullable=False))
    op.drop_constraint('fk__submissions__problem_id__problems', 'submissions', type_='foreignkey')
    op.drop_column('submissions', 'problem_id')
    op.drop_table('problems')


def downgrade() -> None:
    op.create_table('problems',
    sa.Column('contest_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('dt_created', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=False),
    sa.Column('dt_updated', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=False),
    sa.Column('alias', sa.VARCHAR(length=1), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['contest_id'], ['contests.id'], name='fk__problems__contest_id__contests'),
    sa.PrimaryKeyConstraint('id', name='pk__problems'),
    sa.UniqueConstraint('id', name='uq__problems__id')
    )
    op.add_column('submissions', sa.Column('problem_id', sa.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key('fk__submissions__problem_id__problems', 'submissions', 'problems', ['problem_id'], ['id'])
    op.drop_column('submissions', 'problem_alias')
    op.add_column('comments', sa.Column('problem_id', sa.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key('fk__comments__problem_id__problems', 'comments', 'problems', ['problem_id'], ['id'])
    op.drop_column('comments', 'problem_alias')
