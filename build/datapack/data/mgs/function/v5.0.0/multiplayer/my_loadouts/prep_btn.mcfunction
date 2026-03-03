
#> mgs:v5.0.0/multiplayer/my_loadouts/prep_btn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/my_loadouts/build_list
#

# Copy entry data for macro use
data modify storage mgs:temp _btn_data set from storage mgs:temp _iter[0]

# Compute select trigger: 1000 + id
execute store result score #trig mgs.data run data get storage mgs:temp _iter[0].id
scoreboard players add #trig mgs.data 1000
execute store result storage mgs:temp _btn_data.select_trig int 1 run scoreboard players get #trig mgs.data

# Compute toggle visibility trigger: 1400 + id
execute store result score #trig mgs.data run data get storage mgs:temp _iter[0].id
scoreboard players add #trig mgs.data 1400
execute store result storage mgs:temp _btn_data.vis_trig int 1 run scoreboard players get #trig mgs.data

# Compute delete trigger: 1300 + id
execute store result score #trig mgs.data run data get storage mgs:temp _iter[0].id
scoreboard players add #trig mgs.data 1300
execute store result storage mgs:temp _btn_data.delete_trig int 1 run scoreboard players get #trig mgs.data

# Route to correct color variant based on public flag (green=public, red=private)
execute store result score #pub mgs.data run data get storage mgs:temp _iter[0].public
execute if score #pub mgs.data matches 1 run function mgs:v5.0.0/multiplayer/my_loadouts/add_btn_public with storage mgs:temp _btn_data
execute if score #pub mgs.data matches 0 run function mgs:v5.0.0/multiplayer/my_loadouts/add_btn_private with storage mgs:temp _btn_data

