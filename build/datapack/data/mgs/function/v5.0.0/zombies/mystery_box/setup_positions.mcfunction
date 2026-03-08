
#> mgs:v5.0.0/zombies/mystery_box/setup_positions
#
# @within	mgs:v5.0.0/zombies/preload_complete
#

# Summon mystery box markers at map positions
data modify storage mgs:temp _mb_iter set from storage mgs:zombies game.map.mystery_box.positions
execute if data storage mgs:temp _mb_iter[0] run function mgs:v5.0.0/zombies/mystery_box/setup_pos_iter

# Pick a random position as the active mystery box
execute as @e[tag=mgs.mystery_box_pos,sort=random,limit=1] run tag @s add mgs.mystery_box_active

