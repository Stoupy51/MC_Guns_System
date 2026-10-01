
#> mgs:v5.1.0/zombies/mystery_box/setup_positions
#
# @within	mgs:v5.1.0/zombies/preload_complete
#

scoreboard players set #mb_box_counter mgs.data 0

# In box-id order, so names[id - 1] is a box's name ("" when unnamed).
data modify storage mgs:zombies mystery_box.names set value []

data modify storage mgs:temp _mb_iter set from storage mgs:zombies game.map.mystery_box.positions
execute if data storage mgs:temp _mb_iter[0] run function mgs:v5.1.0/zombies/mystery_box/setup_pos_iter

# The active box starts at a random can_start_on position, else any position.
execute as @n[tag=mgs.mystery_box_pos,tag=mgs.mb_can_start,sort=random] run tag @s add mgs.mystery_box_active
execute unless entity @e[tag=mgs.mystery_box_active] as @n[tag=mgs.mystery_box_pos,sort=random] run tag @s add mgs.mystery_box_active

scoreboard players set #mb_pulls mgs.data 0
scoreboard players set #mb_box_counter mgs.data 0
function mgs:v5.1.0/zombies/mystery_box/sync_presence_display

function mgs:v5.1.0/zombies/mystery_box/sync_interaction_visibility

