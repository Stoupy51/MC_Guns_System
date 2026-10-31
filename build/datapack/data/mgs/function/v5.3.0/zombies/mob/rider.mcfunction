
#> mgs:v5.3.0/zombies/mob/rider
#
# @executed	as @n[tag=mgs.zb_new]
#
# @within	mgs:v5.3.0/zombies/mob/riders
#			mgs:v5.3.0/zombies/mob/rider
#

data modify storage mgs:temp _mob set from storage mgs:temp _riders[0][0]
data remove storage mgs:temp _riders[0][0]
data modify storage mgs:temp _mob.no_ai set value 0b
execute unless data storage mgs:temp _mob.entity run data modify storage mgs:temp _mob.entity set value "zombie"

function mgs:v5.3.0/zombies/mob/summon with storage mgs:temp _mob
ride @n[tag=mgs.zb_new] mount @s
scoreboard players set #zb_mob_root mgs.data 0
execute as @n[tag=mgs.zb_new] run function mgs:v5.3.0/zombies/mob/setup

execute if data storage mgs:temp _riders[0][0] run function mgs:v5.3.0/zombies/mob/rider

