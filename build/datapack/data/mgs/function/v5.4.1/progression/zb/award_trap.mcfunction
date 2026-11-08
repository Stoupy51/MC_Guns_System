
#> mgs:v5.4.1/progression/zb/award_trap
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/traps/on_right_click [ as @a[tag=mgs.xp_earner] ]
#

# Activating a trap
scoreboard players add @s mgs.zb.xp_total 2
scoreboard players add @s mgs.zb.xp_prog 2
function mgs:v5.4.1/progression/zb/settle

scoreboard players add @s mgs.st.zb.traps 1

