"""add accreditation fields

Revision ID: add_accreditation
Revises: 800d15796ded
Create Date: 2026-01-16

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_accreditation'
down_revision = '800d15796ded'
branch_labels = None
depends_on = None

def upgrade():
    # Add new columns to psicologos table
    with op.batch_alter_table('psicologos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('numero_licencia', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('institucion', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('documento_acreditacion', sa.String(length=255), nullable=True))

def downgrade():
    # Remove new columns from psicologos table
    with op.batch_alter_table('psicologos', schema=None) as batch_op:
        batch_op.drop_column('documento_acreditacion')
        batch_op.drop_column('institucion')
        batch_op.drop_column('numero_licencia')
