"""create notification sent table

Revision ID: create_notification_sent_table
Revises: increase_string_lengths
Create Date: 2025-07-11 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'create_notification_sent_table'
down_revision = 'increase_string_lengths'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Создаем таблицу notification_sent
    op.create_table('notification_sent',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('notification_type', sa.String(length=50), nullable=False),
        sa.Column('sent_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('event_id', 'notification_type', name='uix_notification_event_type')
    )
    
    # Создаем индекс для быстрого поиска по event_id
    op.create_index(op.f('ix_notification_sent_event_id'), 'notification_sent', ['event_id'], unique=False)

def downgrade() -> None:
    # Удаляем индекс
    op.drop_index(op.f('ix_notification_sent_event_id'), table_name='notification_sent')
    
    # Удаляем таблицу
    op.drop_table('notification_sent') 