
#> mgs:v5.0.0/zombies/mystery_box/setup_pos_iter
#
# @within	mgs:v5.0.0/zombies/mystery_box/setup_positions
#			mgs:v5.0.0/zombies/mystery_box/setup_pos_iter
#

# Read relative position from compound and convert to absolute
execute store result score #mbx mgs.data run data get storage mgs:temp _mb_iter[0].pos[0]
execute store result score #mby mgs.data run data get storage mgs:temp _mb_iter[0].pos[1]
execute store result score #mbz mgs.data run data get storage mgs:temp _mb_iter[0].pos[2]

scoreboard players operation #mbx mgs.data += #gm_base_x mgs.data
scoreboard players operation #mby mgs.data += #gm_base_y mgs.data
scoreboard players operation #mbz mgs.data += #gm_base_z mgs.data

execute store result storage mgs:temp _mbpos.x double 1 run scoreboard players get #mbx mgs.data
execute store result storage mgs:temp _mbpos.y double 1 run scoreboard players get #mby mgs.data
execute store result storage mgs:temp _mbpos.z double 1 run scoreboard players get #mbz mgs.data

function mgs:v5.0.0/zombies/mystery_box/summon_pos_at with storage mgs:temp _mbpos

# Tag entities that can_start_on
data modify storage mgs:temp can_start_on set from storage mgs:temp _mb_iter[0].can_start_on
execute if data storage mgs:temp {can_start_on:1b} run tag @n[tag=mgs.mb_new] add mgs.mb_can_start

# Register Bookshelf events on newly spawned entity
execute as @n[tag=mgs.mb_new] run function #bs.interaction:on_right_click {run:"function mgs:v5.0.0/zombies/mystery_box/on_right_click",executor:"source"}
execute as @n[tag=mgs.mb_new] run function #bs.interaction:on_hover {run:"function mgs:v5.0.0/zombies/mystery_box/on_hover",executor:"source"}
tag @n[tag=mgs.mb_new] remove mgs.mb_new

data remove storage mgs:temp _mb_iter[0]
execute if data storage mgs:temp _mb_iter[0] run function mgs:v5.0.0/zombies/mystery_box/setup_pos_iter

