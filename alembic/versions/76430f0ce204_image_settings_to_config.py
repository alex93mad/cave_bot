"""image settings to config

Revision ID: 76430f0ce204
Revises: 86080e29d660
Create Date: 2024-05-24 21:02:08.222593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from cave_bot.const import SERVER_DEFAULT_USER_CONFIG

# revision identifiers, used by Alembic.
revision: str = '76430f0ce204'
down_revision: Union[str, None] = '86080e29d660'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_config', sa.Column('enemy_icon', sa.Boolean(), nullable=False, server_default = SERVER_DEFAULT_USER_CONFIG['enemy_icon']))
    op.add_column('user_config', sa.Column('enemy_color', sa.String(length=13), nullable=False, server_default = SERVER_DEFAULT_USER_CONFIG['enemy_color']))
    op.add_column('user_config', sa.Column('artifact_icon', sa.Boolean(), nullable=False, server_default = SERVER_DEFAULT_USER_CONFIG['artifact_icon']))
    op.add_column('user_config', sa.Column('artifact_color', sa.String(length=13), nullable=False, server_default = SERVER_DEFAULT_USER_CONFIG['artifact_color']))
    op.add_column('user_config', sa.Column('summon_stone_icon', sa.Boolean(), nullable=False, server_default = SERVER_DEFAULT_USER_CONFIG['summon_stone_icon']))
    op.add_column('user_config', sa.Column('summon_stone_color', sa.String(length=13), nullable=False, server_default = SERVER_DEFAULT_USER_CONFIG['summon_stone_color']))
    op.add_column('user_config', sa.Column('idle_reward_icon', sa.Boolean(), nullable=False, server_default = SERVER_DEFAULT_USER_CONFIG['idle_reward_icon']))
    op.add_column('user_config', sa.Column('idle_reward_color', sa.String(length=13), nullable=False, server_default = SERVER_DEFAULT_USER_CONFIG['idle_reward_color']))
    op.add_column('user_config', sa.Column('empty_color', sa.String(length=13), nullable=False, server_default = SERVER_DEFAULT_USER_CONFIG['empty_color']))
    op.add_column('user_config', sa.Column('me_color', sa.String(length=13), nullable=False, server_default = SERVER_DEFAULT_USER_CONFIG['me_color']))
    op.add_column('user_config', sa.Column('unknown_color', sa.String(length=13), nullable=False, server_default = SERVER_DEFAULT_USER_CONFIG['unknown_color']))
    # ### end Alembic commands ###

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_config', 'unknown_color')
    op.drop_column('user_config', 'me_color')
    op.drop_column('user_config', 'empty_color')
    op.drop_column('user_config', 'idle_reward_color')
    op.drop_column('user_config', 'idle_reward_icon')
    op.drop_column('user_config', 'summon_stone_color')
    op.drop_column('user_config', 'summon_stone_icon')
    op.drop_column('user_config', 'artifact_color')
    op.drop_column('user_config', 'artifact_icon')
    op.drop_column('user_config', 'enemy_color')
    op.drop_column('user_config', 'enemy_icon')
    # ### end Alembic commands ###
