"""Insert data into products table

Revision ID: 6cabd0d66086
Revises: a1b2c3d4e5f6
Create Date: 2026-11-19 15:28:12.267254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cabd0d66086'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade():
    # Вставляємо два нові продукти (active=1, created_at поточна дата)
    op.execute("INSERT INTO products (name, price, active, created_at) VALUES ('Xiaomi', 600, 1, CURRENT_TIMESTAMP)")
    op.execute("INSERT INTO products (name, price, active, created_at) VALUES ('Samsung', 900, 1, CURRENT_TIMESTAMP)")


def downgrade():
    # Відкат: видаляємо ці продукти
    op.execute("DELETE FROM products WHERE name IN ('Xiaomi', 'Samsung')")