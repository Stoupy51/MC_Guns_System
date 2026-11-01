
#> mgs:v5.3.0/maps/editor/dedupe/player_spawn_zb
#
# @executed	at @s
#
# @within	mgs:v5.3.0/maps/editor/remove_duplicates [ at @s ]
#

execute if entity @s[tag=mgs.ed_dup] run return 0
tag @s add mgs.ed_keep
execute unless entity @e[type=minecraft:marker,tag=mgs.element.player_spawn_zb,tag=!mgs.ed_keep,distance=..0.01] run return 0
function mgs:v5.3.0/maps/editor/dedupe_read
execute as @e[type=minecraft:marker,tag=mgs.element.player_spawn_zb,tag=!mgs.ed_keep,distance=..0.01] run function mgs:v5.3.0/maps/editor/dedupe_same

