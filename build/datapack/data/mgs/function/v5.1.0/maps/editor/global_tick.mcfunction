
#> mgs:v5.1.0/maps/editor/global_tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/maps/editor/tick
#

# Claim this tick so the remaining editors skip straight past the call above
scoreboard players operation #ed_global_tick mgs.data = #total_tick mgs.data

# Model displays: rebuild once per second so rotation/config edits on markers stay in sync.
# The marker rotation sync is an NBT read plus an NBT write per marker, which is far too expensive
# to run every tick — and yaw only ever changes when someone edits it, so once a second is plenty.
scoreboard players operation #ed_disp_phase mgs.data = #total_tick mgs.data
scoreboard players operation #ed_disp_phase mgs.data %= #20 mgs.data
execute if score #ed_disp_phase mgs.data matches 0 as @e[type=minecraft:marker,tag=mgs.map_element] run data modify entity @s Rotation[0] set from entity @s data.yaw
execute if score #ed_disp_phase mgs.data matches 0 run function mgs:v5.1.0/maps/editor/refresh_displays

# Marker particles every 4 ticks: dust lingers about a second, so this looks identical to emitting
# them every tick while cutting the particle commands (and the packets they generate) by 4x.
scoreboard players operation #ed_part_phase mgs.data = #total_tick mgs.data
scoreboard players operation #ed_part_phase mgs.data %= #4 mgs.data
execute if score #ed_part_phase mgs.data matches 0 run function mgs:v5.1.0/maps/editor/particles

