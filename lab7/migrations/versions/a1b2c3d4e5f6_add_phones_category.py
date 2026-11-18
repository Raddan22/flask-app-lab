"""Add Phones category

Revision ID: a1b2c3d4e5f6
Revises: 43ad89061d75
Create Date: 2026-11-18 21:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'a1b2c3d4e5f6'
down_revision = '43ad89061d75'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("INSERT INTO categories (name) VALUES ('Phones')")


def downgrade():
    op.execute("DELETE FROM categories WHERE name = 'Phones'")