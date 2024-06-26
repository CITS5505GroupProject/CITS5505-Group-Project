"""initialize database

Revision ID: 3af978d7fafc
Revises: 
Create Date: 2024-04-30 16:12:53.795132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3af978d7fafc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pk'),
    sa.UniqueConstraint('email', name='user_email_uc'),
    sa.UniqueConstraint('username', name='user_username_uc')
    )
    op.create_table('survey',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='survey_user_fk'),
    sa.PrimaryKeyConstraint('id', name='survey_pk')
    )
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=255), nullable=False),
    sa.Column('survey_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['survey_id'], ['survey.id'], name='question_survey_fk'),
    sa.PrimaryKeyConstraint('id', name='question_pk')
    )
    op.create_table('answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=255), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], name='answer_question_fk'),
    sa.PrimaryKeyConstraint('id', name='answer_pk')
    )
    op.create_table('response',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('answer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['answer_id'], ['answer.id'], name='response_answer_fk'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='response_user_fk'),
    sa.PrimaryKeyConstraint('id', name='response_pk')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('response')
    op.drop_table('answer')
    op.drop_table('question')
    op.drop_table('survey')
    op.drop_table('user')
    # ### end Alembic commands ###
