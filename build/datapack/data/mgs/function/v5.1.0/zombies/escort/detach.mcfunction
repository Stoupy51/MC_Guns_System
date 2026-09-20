
#> mgs:v5.1.0/zombies/escort/detach
#
# @executed	as @e[tag=mgs.zb_escorted] & at @s
#
# @within	mgs:v5.1.0/zombies/escort/zombie_tick
#			mgs:v5.1.0/zombies/escort/release
#			mgs:v5.1.0/zombies/escort/give_up
#			mgs:v5.1.0/zombies/escort/end_at_trader [ as @e[tag=mgs.zb_escorted,distance=..8,limit=1,sort=nearest] ]
#

tag @s remove mgs.zb_escorted
data modify entity @s NoAI set value 0b
scoreboard players remove #zb_escort_count mgs.data 1

# Kickstart vanilla AI. A zombie fresh off NoAI won't re-scan for a target for up to ~0.5s
# (NearestAttackableTargetGoal's mustSee re-scan interval) and looks braindead standing still.
# Turn it to face the nearest player and clear its NoActionTime so the goal selector re-evaluates
# immediately, then a brief speed nudge so it lunges the instant it acquires the target instead
# of pausing. (NoActionTime being high after the frozen transport is what stalls the first scan.)
data modify entity @s NoActionTime set value 0
execute at @s facing entity @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] eyes run tp @s ~ ~ ~ ~ ~
effect give @s minecraft:speed 2 0 true

# Fresh stuck-tracking window from wherever the escort left the zombie
scoreboard players set @s mgs.zb.stuck_dist 4
execute store result score @s mgs.zb.stuck_x run data get entity @s Pos[0]
execute store result score @s mgs.zb.stuck_z run data get entity @s Pos[2]
scoreboard players operation @s mgs.zb.stuck_ticks = #total_tick mgs.data

