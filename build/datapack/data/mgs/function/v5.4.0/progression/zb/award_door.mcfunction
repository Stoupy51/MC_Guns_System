
#> mgs:v5.4.0/progression/zb/award_door
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/doors/on_right_click [ as @a[tag=mgs.xp_earner] ]
#

# Opening a door or clearing debris
scoreboard players add @s mgs.zb.xp_total 3
scoreboard players add @s mgs.zb.xp_prog 3
function mgs:v5.4.0/progression/zb/settle

scoreboard players add @s mgs.st.zb.doors 1

