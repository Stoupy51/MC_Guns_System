
#> mgs:v5.4.1/progression/zb/award_powerup
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/powerups/do_pickup [ as @a[tag=mgs.pu_collecting] ]
#

# Picking up any power-up
scoreboard players add @s mgs.zb.xp_total 3
scoreboard players add @s mgs.zb.xp_prog 3
function mgs:v5.4.1/progression/zb/settle

scoreboard players add @s mgs.st.zb.powerups 1

