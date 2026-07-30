
#> mgs:v5.1.0/zombies/vocals/death
#
# @executed	as @e[tag=...,scores={mgs.zb.death_time=-15}] & at @s
#
# @within	mgs:v5.1.0/zombies/death_watch_tick [ as @e[tag=...,scores={mgs.zb.death_time=-15}] & at @s ]
#

# Consume the trigger value so a zombie whose death-watch marker got separated can't loop the groan:
# the sweep overwrites this every tick for anything still mounted, so this only matters when it doesn't.
scoreboard players set @s mgs.zb.death_time 0

execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..32] unless score @s mgs.zb.vox_death > #total_tick mgs.data run function mgs:v5.1.0/zombies/vocals/death_for

