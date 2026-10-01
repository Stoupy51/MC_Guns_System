
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

# A zombie fresh off NoAI stands still for up to 0.5 s before re-scanning for a target. Clearing NoActionTime
# (high after the frozen ride) makes the goals re-evaluate at once, and a brief speed nudge makes it lunge.
data modify entity @s NoActionTime set value 0
execute at @s facing entity @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] eyes run tp @s ~ ~ ~ ~ ~
effect give @s minecraft:speed 2 0 true

# Fresh stuck window from where the escort left it.
scoreboard players set @s mgs.zb.stuck_dist 4
execute store result score @s mgs.zb.stuck_x run data get entity @s Pos[0]
execute store result score @s mgs.zb.stuck_z run data get entity @s Pos[2]
scoreboard players operation @s mgs.zb.stuck_ticks = #total_tick mgs.data

