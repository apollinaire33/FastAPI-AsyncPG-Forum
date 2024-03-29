"""add user model

Revision ID: efa1751fcaf2
Revises: 8ea161af29bb
Create Date: 2022-05-08 18:21:39.664767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efa1751fcaf2'
down_revision = '8ea161af29bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('role', sa.Enum('admin', 'user', name='rolesenum'), server_default='user', nullable=False),
    sa.Column('date_joined', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('active', sa.Boolean(), server_default='true', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
