
#> mgs:v5.0.1/utils/coord_stick_relative
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/utils/coord_stick {run:"function mgs:v5.0.1/utils/coord_stick_relative",with:{}}
#

# State: 0 = first click, 1 = second click (origin already saved)
scoreboard players set #cs_state mgs.data 0
execute if data storage mgs:temp coord_stick.origin run scoreboard players set #cs_state mgs.data 1

# Particle at block center
execute align xyz run particle firework ~.5 ~.5 ~.5 0.4 0.4 0.4 0.01 100 force @a[distance=..20]

# --- Second click: compute relative offset ---
execute if score #cs_state mgs.data matches 1 summon marker run function mgs:v5.0.1/utils/coord_stick_store_pos
execute if score #cs_state mgs.data matches 1 run scoreboard players operation #cs_dest_x mgs.data = #cs_pos_x mgs.data
execute if score #cs_state mgs.data matches 1 run scoreboard players operation #cs_dest_y mgs.data = #cs_pos_y mgs.data
execute if score #cs_state mgs.data matches 1 run scoreboard players operation #cs_dest_z mgs.data = #cs_pos_z mgs.data
execute if score #cs_state mgs.data matches 1 store result score #cs_orig_x mgs.data run data get storage mgs:temp coord_stick.origin[0]
execute if score #cs_state mgs.data matches 1 store result score #cs_orig_y mgs.data run data get storage mgs:temp coord_stick.origin[1]
execute if score #cs_state mgs.data matches 1 store result score #cs_orig_z mgs.data run data get storage mgs:temp coord_stick.origin[2]
execute if score #cs_state mgs.data matches 1 run scoreboard players operation #cs_dest_x mgs.data -= #cs_orig_x mgs.data
execute if score #cs_state mgs.data matches 1 run scoreboard players operation #cs_dest_y mgs.data -= #cs_orig_y mgs.data
execute if score #cs_state mgs.data matches 1 run scoreboard players operation #cs_dest_z mgs.data -= #cs_orig_z mgs.data
execute if score #cs_state mgs.data matches 1 run data modify storage mgs:temp coord_stick.result set value {x:0,y:0,z:0}
execute if score #cs_state mgs.data matches 1 store result storage mgs:temp coord_stick.result.x int 1 run scoreboard players get #cs_dest_x mgs.data
execute if score #cs_state mgs.data matches 1 store result storage mgs:temp coord_stick.result.y int 1 run scoreboard players get #cs_dest_y mgs.data
execute if score #cs_state mgs.data matches 1 store result storage mgs:temp coord_stick.result.z int 1 run scoreboard players get #cs_dest_z mgs.data
execute if score #cs_state mgs.data matches 1 as @a[tag=mgs.coord_stick_user,limit=1] run function mgs:v5.0.1/utils/coord_stick_print with storage mgs:temp coord_stick.result
execute if score #cs_state mgs.data matches 1 run data remove storage mgs:temp coord_stick.result
execute if score #cs_state mgs.data matches 1 run data remove storage mgs:temp coord_stick.origin

# --- First click: record origin position ---
execute if score #cs_state mgs.data matches 0 summon marker run function mgs:v5.0.1/utils/coord_stick_store_pos
execute if score #cs_state mgs.data matches 0 run data modify storage mgs:temp coord_stick.origin set value [0,0,0]
execute if score #cs_state mgs.data matches 0 store result storage mgs:temp coord_stick.origin[0] int 1 run scoreboard players get #cs_pos_x mgs.data
execute if score #cs_state mgs.data matches 0 store result storage mgs:temp coord_stick.origin[1] int 1 run scoreboard players get #cs_pos_y mgs.data
execute if score #cs_state mgs.data matches 0 store result storage mgs:temp coord_stick.origin[2] int 1 run scoreboard players get #cs_pos_z mgs.data
execute if score #cs_state mgs.data matches 0 as @a[tag=mgs.coord_stick_user,limit=1] run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.first_position_saved_right_click_again_to_get_the_offset","color":"yellow"}]

