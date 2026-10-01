""" Liking a loadout once per player and incrementing its counter. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.catalogs import TRIG_LIKE_BASE
from ....helpers import MGS_TAG


# Functions
def write_loadout_likes() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## One like per player.
	write_versioned_function("multiplayer/custom/like", f"""
# The trigger value carries the loadout id.
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_LIKE_BASE}

# Mark it in the player's liked[], unless already there.
data modify storage {ns}:temp _pd_src set from storage {ns}:multiplayer player_data
data modify storage {ns}:multiplayer player_data set value []
scoreboard players set #already_liked {ns}.data 0
execute if data storage {ns}:temp _pd_src[0] run function {ns}:v{version}/multiplayer/custom/like_pd_rebuild

# Then raise the loadout's like count.
execute if score #already_liked {ns}.data matches 0 run function {ns}:v{version}/multiplayer/custom/like_increment_setup

execute if score #already_liked {ns}.data matches 0 run tellraw @s ["",{MGS_TAG},{{"text":"Loadout liked!","color":"green"}}]
execute if score #already_liked {ns}.data matches 1 run tellraw @s ["",{MGS_TAG},{{"text":"You already liked this loadout","color":"yellow"}}]

function {ns}:v{version}/multiplayer/marketplace/browse
""")

	write_versioned_function("multiplayer/custom/like_pd_rebuild", f"""
execute store result score #pd_pid {ns}.data run data get storage {ns}:temp _pd_src[0].pid
execute if score #pd_pid {ns}.data = @s {ns}.mp.pid run function {ns}:v{version}/multiplayer/custom/like_modify_entry

data modify storage {ns}:multiplayer player_data append from storage {ns}:temp _pd_src[0]

data remove storage {ns}:temp _pd_src[0]
execute if data storage {ns}:temp _pd_src[0] run function {ns}:v{version}/multiplayer/custom/like_pd_rebuild
""")

	write_versioned_function("multiplayer/custom/like_modify_entry", f"""
data modify storage {ns}:temp _liked_iter set from storage {ns}:temp _pd_src[0].liked
execute if data storage {ns}:temp _liked_iter[0] run function {ns}:v{version}/multiplayer/custom/like_check_each

execute if score #already_liked {ns}.data matches 0 run function {ns}:v{version}/multiplayer/custom/like_append_new
""")

	write_versioned_function("multiplayer/custom/like_append_new", f"""
data modify storage {ns}:temp _new_liked set value {{id:0}}
execute store result storage {ns}:temp _new_liked.id int 1 run scoreboard players get #loadout_id {ns}.data
data modify storage {ns}:temp _pd_src[0].liked append from storage {ns}:temp _new_liked
""")

	write_versioned_function("multiplayer/custom/like_check_each", f"""
execute store result score #liked_id {ns}.data run data get storage {ns}:temp _liked_iter[0].id
execute if score #liked_id {ns}.data = #loadout_id {ns}.data run scoreboard players set #already_liked {ns}.data 1

data remove storage {ns}:temp _liked_iter[0]
execute if data storage {ns}:temp _liked_iter[0] unless score #already_liked {ns}.data matches 1 run function {ns}:v{version}/multiplayer/custom/like_check_each
""")

	write_versioned_function("multiplayer/custom/like_increment_setup", f"""
data modify storage {ns}:temp _like_src set from storage {ns}:multiplayer custom_loadouts
data modify storage {ns}:multiplayer custom_loadouts set value []
execute if data storage {ns}:temp _like_src[0] run function {ns}:v{version}/multiplayer/custom/like_increment_rebuild
""")

	write_versioned_function("multiplayer/custom/like_increment_rebuild", f"""
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _like_src[0].id
execute if score #entry_id {ns}.data = #loadout_id {ns}.data run function {ns}:v{version}/multiplayer/custom/like_increment_entry

data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _like_src[0]

data remove storage {ns}:temp _like_src[0]
execute if data storage {ns}:temp _like_src[0] run function {ns}:v{version}/multiplayer/custom/like_increment_rebuild
""")

	write_versioned_function("multiplayer/custom/like_increment_entry", f"""
# Older entries may have no likes field.
execute unless data storage {ns}:temp _like_src[0].likes run data modify storage {ns}:temp _like_src[0].likes set value 0
execute store result score #likes {ns}.data run data get storage {ns}:temp _like_src[0].likes
scoreboard players add #likes {ns}.data 1
execute store result storage {ns}:temp _like_src[0].likes int 1 run scoreboard players get #likes {ns}.data
""")

