
#> mgs:v5.3.0/maps/editor/name/rounds
#
# @executed	as @e[type=minecraft:marker,tag=mgs.map_element]
#
# @within	mgs:v5.3.0/maps/editor/refresh_marker
#

execute store result score #ed_rmin mgs.data run data get entity @s data.min_round
scoreboard players set #ed_rmax mgs.data 0
execute if data entity @s data.max_round store result score #ed_rmax mgs.data run data get entity @s data.max_round
execute if score #ed_rmin mgs.data matches ..0 if score #ed_rmax mgs.data matches ..0 run return 0
execute if score #ed_rmin mgs.data matches ..0 run scoreboard players set #ed_rmin mgs.data 1
execute store result storage mgs:temp _ed_rounds.min int 1 run scoreboard players get #ed_rmin mgs.data
execute store result storage mgs:temp _ed_rounds.max int 1 run scoreboard players get #ed_rmax mgs.data
execute if score #ed_rmax mgs.data matches ..0 run return run function mgs:v5.3.0/maps/editor/name/rounds_from with storage mgs:temp _ed_rounds
function mgs:v5.3.0/maps/editor/name/rounds_between with storage mgs:temp _ed_rounds

