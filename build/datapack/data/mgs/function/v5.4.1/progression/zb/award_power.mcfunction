
#> mgs:v5.4.1/progression/zb/award_power
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/power/on_activate [ as @a[scores={mgs.zb.in_game=1}] ]
#

# Flipping the power switch; one-off, and the whole team earns it
scoreboard players add @s mgs.zb.xp_total 10
scoreboard players add @s mgs.zb.xp_prog 10
function mgs:v5.4.1/progression/zb/settle

scoreboard players add @s mgs.st.zb.power 1

