
#> mgs:v5.0.1/zombies/mystery_box/setup_positions
#
# @within	mgs:v5.0.1/zombies/preload_complete
#

# Summon mystery box markers at map positions
scoreboard players set #mb_box_counter mgs.data 0
data modify storage mgs:temp _mb_iter set from storage mgs:zombies game.map.mystery_box.positions
execute if data storage mgs:temp _mb_iter[0] run function mgs:v5.0.1/zombies/mystery_box/setup_pos_iter

# Pick a random position with can_start_on as the active mystery box
execute as @n[tag=mgs.mystery_box_pos,tag=mgs.mb_can_start,sort=random] run tag @s add mgs.mystery_box_active
# Fallback if no can_start_on positions exist
execute unless entity @e[tag=mgs.mystery_box_active] as @n[tag=mgs.mystery_box_pos,sort=random] run tag @s add mgs.mystery_box_active

# Init pull counter and box-id counter, then spawn presence chest at the active position.
scoreboard players set #mb_pulls mgs.data 0
scoreboard players set #mb_box_counter mgs.data 0
function mgs:v5.0.1/zombies/mystery_box/sync_presence_display

