
#> mgs:v5.1.0/zombies/rescue_tp
#
# @executed	at @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/on_stuck_zombie [ at @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] ]
#			mgs:v5.1.0/zombies/on_stuck_zombie
#

tp @s @n[tag=mgs.zb_near]
scoreboard players operation @s mgs.zb.spawn.sid = @n[tag=mgs.zb_near] mgs.zb.spawn.sid

