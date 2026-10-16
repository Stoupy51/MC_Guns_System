
#> mgs:v5.1.0/zombies/absorb_above_cap
#
# @executed	as @n[tag=mgs.zb_near,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/apply_zombie_hp
#			mgs:v5.1.0/zombies/types/dog
#

scoreboard players operation #zb_absorb mgs.data = @s mgs.zb.max_hp
scoreboard players remove #zb_absorb mgs.data 1024
execute unless score #zb_absorb mgs.data matches 1.. run return 0
execute store result storage mgs:temp _zb_absorb.val int 1 run scoreboard players get #zb_absorb mgs.data
function mgs:v5.1.0/zombies/apply_zombie_absorption with storage mgs:temp _zb_absorb

