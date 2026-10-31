
#> mgs:v5.3.0/zombies/mob/spawn
#
# @executed	positioned ~ ~-1.8 ~
#
# @within	mgs:v5.3.0/zombies/arrival/floor [ positioned ~ ~-1.8 ~ ]
#			mgs:v5.3.0/zombies/arrival/ceiling [ positioned ~ ~2.2 ~ ]
#			mgs:v5.3.0/zombies/arrival/instant
#			mgs:v5.3.0/zombies/portal_strike [ positioned ~ ~0.2 ~ ]
#

function mgs:v5.3.0/zombies/mob/summon with storage mgs:temp _mob
tag @n[tag=mgs.zb_new] add mgs.zb_new_root
scoreboard players set #zb_mob_root mgs.data 1
execute as @n[tag=mgs.zb_new] run function mgs:v5.3.0/zombies/mob/setup

