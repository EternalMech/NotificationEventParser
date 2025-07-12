"""increase string lengths for event fields

Revision ID: increase_string_lengths
Revises: da76e3df044b
Create Date: 2025-07-11 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'increase_string_lengths'
down_revision = 'da76e3df044b'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('events', 'name', type_=sa.String(length=2000))
    op.alter_column('events', 'interests', type_=sa.String(length=500))
    op.alter_column('events', 'address', type_=sa.String(length=500))
    op.alter_column('events', 'join_type', type_=sa.String(length=100))
    op.alter_column('events', 'join_link', type_=sa.String(length=500))
    op.alter_column('events', 'photo', type_=sa.String(length=500))

def downgrade():
    op.alter_column('events', 'name', type_=sa.String(length=255))
    op.alter_column('events', 'interests', type_=sa.String(length=255))
    op.alter_column('events', 'address', type_=sa.String(length=255))
    op.alter_column('events', 'join_type', type_=sa.String(length=255))
    op.alter_column('events', 'join_link', type_=sa.String(length=255))
    op.alter_column('events', 'photo', type_=sa.String(length=255)) 