
#> mgs:v5.3.0/zombies/rescue_tp
#
# @executed	at @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator]
#
# @within	mgs:v5.3.0/zombies/on_stuck_zombie [ at @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] ]
#			mgs:v5.3.0/zombies/on_stuck_zombie
#

tp @s @n[tag=mgs.zb_near]
scoreboard players operation @s mgs.zb.spawn.sid = @n[tag=mgs.zb_near] mgs.zb.spawn.sid
tag @s add mgs.zb_rescue_new
execute as @n[tag=mgs.zb_near] at @s run function mgs:v5.3.0/zombies/arrival/rescued
tag @s remove mgs.zb_rescue_new

