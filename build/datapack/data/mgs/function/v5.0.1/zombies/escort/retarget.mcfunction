
#> mgs:v5.0.1/zombies/escort/retarget
#
# @executed	as @n[tag=mgs.zb_escort_new] & at @s
#
# @within	mgs:v5.0.1/zombies/escort/start [ as @n[tag=mgs.zb_escort_new] & at @s ]
#			mgs:v5.0.1/zombies/escort/zombie_tick [ at @s ]
#

execute store result storage mgs:temp _escort.x int 1 run data get entity @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] Pos[0]
execute store result storage mgs:temp _escort.y int 1 run data get entity @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] Pos[1]
execute store result storage mgs:temp _escort.z int 1 run data get entity @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] Pos[2]
function mgs:v5.0.1/zombies/escort/set_wander_target with storage mgs:temp _escort

