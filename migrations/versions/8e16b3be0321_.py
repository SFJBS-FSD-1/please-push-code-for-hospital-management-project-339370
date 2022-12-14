"""empty message

Revision ID: 8e16b3be0321
Revises: 
Create Date: 2022-10-04 02:07:19.478155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e16b3be0321'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('patients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.BigInteger(), nullable=False),
    sa.Column('aadhar', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('admit_date', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('discharge_date', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('bed_type', sa.String(length=80), nullable=False),
    sa.Column('address', sa.String(length=250), nullable=False),
    sa.Column('city', sa.String(length=250), nullable=False),
    sa.Column('state', sa.String(length=250), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('aadhar')
    )
    op.create_table('diagnostics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('test_name', sa.String(length=80), nullable=False),
    sa.Column('test_id', sa.Integer(), nullable=False),
    sa.Column('test_charge', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('medicines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('med_name', sa.String(length=80), nullable=False),
    sa.Column('med_id', sa.Integer(), nullable=False),
    sa.Column('rate', sa.Integer(), nullable=False),
    sa.Column('Dosage', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('medicines')
    op.drop_table('diagnostics')
    op.drop_table('patients')
    op.drop_table('admin')
    # ### end Alembic commands ###
