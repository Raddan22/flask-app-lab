"""Initial migration with Product and Category

Revision ID: 43ad89061d75
Revises: 
Create Date: 2026-11-18 21:21:32.120769

"""
from alembic import op
import sqlalchemy as sa


revision = '43ad89061d75'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=150), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('posted', sa.DateTime(), nullable=False),
    sa.Column('category', sa.Enum('news', 'publication', 'tech', 'other', name='category_enum'), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('author', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('products')
    op.drop_table('posts')
    op.drop_table('categories')