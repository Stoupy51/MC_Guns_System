
#> mgs:v5.4.2/zombies/barricades/break
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/barricades/destroy
#			mgs:v5.4.2/zombies/save/restore [ as @e[type=minecraft:block_display,tag=mgs.barricade_display,scores={mgs.zb.barricade.state=1}] ]
#

scoreboard players set @s mgs.zb.barricade.state 1
scoreboard players set @s mgs.zb.barricade.r_timer 0
data modify entity @s block_state set from entity @s data.block_disabled

