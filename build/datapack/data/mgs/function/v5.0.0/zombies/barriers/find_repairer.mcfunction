
#> mgs:v5.0.0/zombies/barriers/find_repairer
#
# @executed	as @e[tag=mgs.barrier_display] & at @s
#
# @within	mgs:v5.0.0/zombies/barriers/destroyed_tick with storage mgs:temp _brptick
#
# @args		radius (unknown)
#

# MACRO: @s = destroyed barrier marker, $(radius) = sphere radius
# Picks nearest sneaking in-game player and assigns them as repairer
scoreboard players set #barrier_found_repairer mgs.data 0
$execute as @a[scores={mgs.zb.in_game=1},predicate=mgs:v5.0.0/is_sneaking,distance=..$(radius),tag=!mgs.barrier_repairing,limit=1,sort=nearest] run function mgs:v5.0.0/zombies/barriers/start_repairing_player
execute if score #barrier_found_repairer mgs.data matches 1 run scoreboard players set @s mgs.zb.barrier.rp_timer 30

