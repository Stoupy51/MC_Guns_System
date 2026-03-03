
#> mgs:v5.0.0/multiplayer/marketplace/prep_btn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/marketplace/build_list
#

# Copy entry data for macro use
data modify storage mgs:temp _btn_data set from storage mgs:temp _iter[0]

# Compute select trigger: 1000 + id
execute store result score #trig mgs.data run data get storage mgs:temp _iter[0].id
scoreboard players add #trig mgs.data 1000
execute store result storage mgs:temp _btn_data.select_trig int 1 run scoreboard players get #trig mgs.data

# Compute like trigger: 1200 + id
execute store result score #trig mgs.data run data get storage mgs:temp _iter[0].id
scoreboard players add #trig mgs.data 1200
execute store result storage mgs:temp _btn_data.like_trig int 1 run scoreboard players get #trig mgs.data

# Compute favorite trigger: 1100 + id
execute store result score #trig mgs.data run data get storage mgs:temp _iter[0].id
scoreboard players add #trig mgs.data 1100
execute store result storage mgs:temp _btn_data.fav_trig int 1 run scoreboard players get #trig mgs.data

# Add buttons to dialog
function mgs:v5.0.0/multiplayer/marketplace/add_btn with storage mgs:temp _btn_data

