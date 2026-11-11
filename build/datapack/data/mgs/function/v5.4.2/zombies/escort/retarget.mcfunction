
#> mgs:v5.4.2/zombies/escort/retarget
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/escort/start [ as @n[tag=mgs.zb_escort_new] & at @s ]
#			mgs:v5.4.2/zombies/escort/escort_tail [ at @s ]
#

# The monkey flag outranks the PaP lure and player targeting.
execute if entity @s[tag=mgs.zb_escort_monkey] run return run function mgs:v5.4.2/zombies/escort/retarget_monkey

# Walk-to: the trader carries the fixed destination (WanderToPositionGoal.stop() nulls wander_target).
execute if entity @s[tag=mgs.zb_escort_walk] run return run function mgs:v5.4.2/zombies/escort/set_wander_target with entity @s data.walk_to

execute if score #zb_lure mgs.data matches 1 if entity @e[tag=mgs.lure_center] run return run function mgs:v5.4.2/zombies/escort/retarget_lure
execute at @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] summon minecraft:marker run function mgs:v5.4.2/shared/probe_pos
execute store result storage mgs:temp _escort.x int 1 run data get storage mgs:temp _probe_pos[0]
execute store result storage mgs:temp _escort.y int 1 run data get storage mgs:temp _probe_pos[1]
execute store result storage mgs:temp _escort.z int 1 run data get storage mgs:temp _probe_pos[2]
function mgs:v5.4.2/zombies/escort/set_wander_target with storage mgs:temp _escort

