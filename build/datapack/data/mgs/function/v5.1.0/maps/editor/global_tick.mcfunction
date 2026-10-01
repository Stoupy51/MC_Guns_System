
#> mgs:v5.1.0/maps/editor/global_tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/maps/editor/tick
#

# The other editors skip the call above.
scoreboard players operation #ed_global_tick mgs.data = #total_tick mgs.data

# Checked once a second and rebuilt only after an edit: syncing a marker's rotation is an NBT read and write, and yaw only changes on edits.
scoreboard players operation #ed_disp_phase mgs.data = #total_tick mgs.data
scoreboard players operation #ed_disp_phase mgs.data %= #20 mgs.data
execute if score #ed_disp_phase mgs.data matches 0 as @e[type=minecraft:marker,tag=mgs.map_element] run data modify entity @s Rotation[0] set from entity @s data.yaw
execute if score #ed_disp_phase mgs.data matches 0 run function mgs:v5.1.0/maps/editor/displays/sync

# Every 4 ticks: dust lingers about a second, so it looks the same with a quarter of the commands and packets.
scoreboard players operation #ed_part_phase mgs.data = #total_tick mgs.data
scoreboard players operation #ed_part_phase mgs.data %= #4 mgs.data
execute if score #ed_part_phase mgs.data matches 0 run function mgs:v5.1.0/maps/editor/particles

