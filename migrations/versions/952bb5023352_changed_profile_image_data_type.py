"""changed profile_image data type.

Revision ID: 952bb5023352
Revises: fc447bc6e783
Create Date: 2023-08-14 12:45:26.528606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '952bb5023352'
down_revision = 'fc447bc6e783'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('profile_image',
               existing_type=sa.BLOB(),
               type_=sa.String(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('profile_image',
               existing_type=sa.String(length=255),
               type_=sa.BLOB(),
               existing_nullable=True)

    # ### end Alembic commands ###