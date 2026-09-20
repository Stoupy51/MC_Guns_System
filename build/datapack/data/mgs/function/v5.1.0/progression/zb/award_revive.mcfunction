
#> mgs:v5.1.0/progression/zb/award_revive
#
# @executed	as @a[tag=mgs.xp_earner]
#
# @within	mgs:v5.1.0/zombies/revive/revive_complete [ as @a[tag=mgs.xp_earner] ]
#

# Getting a teammate back on their feet
scoreboard players add @s mgs.zb.xp_total 10
scoreboard players add @s mgs.zb.xp_prog 10

# Observers of this award
scoreboard players add @s mgs.adv.zb.revives 1
function mgs:v5.1.0/progression/zb/settle

