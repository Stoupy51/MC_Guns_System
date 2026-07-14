
#> mgs:v5.1.0/zombies/filter_spawn_abox
#
# @executed	as @e[tag=mgs.zb_near]
#
# @within	mgs:v5.1.0/zombies/spawn_zombie [ as @e[tag=mgs.zb_near] ]
#

data modify storage mgs:temp _abox_chk set from entity @s data.abox
scoreboard players set #abox_ok mgs.data 0
function mgs:v5.1.0/zombies/test_spawn_abox with storage mgs:temp _abox_chk
execute if score #abox_ok mgs.data matches 0 run tag @s remove mgs.zb_near

