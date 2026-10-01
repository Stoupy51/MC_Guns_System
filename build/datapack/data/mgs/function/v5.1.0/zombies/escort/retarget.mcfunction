
#> mgs:v5.1.0/zombies/escort/retarget
#
# @executed	as @n[tag=mgs.zb_escort_new] & at @s
#
# @within	mgs:v5.1.0/zombies/escort/start [ as @n[tag=mgs.zb_escort_new] & at @s ]
#			mgs:v5.1.0/zombies/escort/escort_tail [ at @s ]
#

# The monkey flag outranks the PaP lure and player targeting.
execute if entity @s[tag=mgs.zb_escort_monkey] run return run function mgs:v5.1.0/zombies/escort/retarget_monkey

# Walk-to: the trader carries the fixed destination (WanderToPositionGoal.stop() nulls wander_target).
execute if entity @s[tag=mgs.zb_escort_walk] run return run function mgs:v5.1.0/zombies/escort/set_wander_target with entity @s data.walk_to

execute if score #zb_lure mgs.data matches 1 if entity @e[tag=mgs.lure_center] run return run function mgs:v5.1.0/zombies/escort/retarget_lure
execute store result storage mgs:temp _escort.x int 1 run data get entity @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] Pos[0]
execute store result storage mgs:temp _escort.y int 1 run data get entity @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] Pos[1]
execute store result storage mgs:temp _escort.z int 1 run data get entity @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] Pos[2]
function mgs:v5.1.0/zombies/escort/set_wander_target with storage mgs:temp _escort

