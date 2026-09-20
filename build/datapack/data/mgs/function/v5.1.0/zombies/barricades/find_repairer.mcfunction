
#> mgs:v5.1.0/zombies/barricades/find_repairer
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/barricades/destroyed_tick with storage mgs:temp _brptick
#
# @args		radius (unknown)
#

# MACRO: @s = destroyed barricade marker, $(radius) = sphere radius
# Picks nearest sneaking in-game player and assigns them as repairer
scoreboard players set #barricade_found_repairer mgs.data 0
$execute as @a[scores={mgs.zb.in_game=1},predicate=mgs:v5.1.0/is_sneaking,distance=..$(radius),tag=!mgs.barricade_repairing,limit=1,sort=nearest] run function mgs:v5.1.0/zombies/barricades/start_repairing_player
execute if score #barricade_found_repairer mgs.data matches 1 run scoreboard players set @s mgs.zb.barricade.rp_timer 30

