
#> mgs:v5.1.0/progression/zb/award_powerup
#
# @executed	as @a[tag=mgs.pu_collecting]
#
# @within	mgs:v5.1.0/zombies/powerups/do_pickup [ as @a[tag=mgs.pu_collecting] ]
#

# Picking up any power-up
scoreboard players add @s mgs.zb.xp_total 3
scoreboard players add @s mgs.zb.xp_prog 3
function mgs:v5.1.0/progression/zb/settle

