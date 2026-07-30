
#> mgs:v5.1.0/zombies/barricades/destroyed_tick
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/barricades/tick
#			mgs:v5.1.0/zombies/barricades/destroyed_tick [ positioned ~ ~-1 ~ ]
#

# Delegate detection downward if floating (upper barricades in a column share floor-level repair
# detection) so a player standing on the ground can reach and repair a barricade stacked above them.
execute positioned ~ ~-1 ~ if block ~ ~ ~ air run return run function mgs:v5.1.0/zombies/barricades/destroyed_tick

# @s = destroyed barricade display, at @s
execute store result score #barricade_id mgs.data run scoreboard players get @s mgs.zb.barricade.id
execute store result storage mgs:temp _brptick.radius int 1 run scoreboard players get @s mgs.zb.barricade.radius

# Handle repair timer or find a new repairer (both macros using radius)
execute if score @s mgs.zb.barricade.rp_timer matches 1.. run function mgs:v5.1.0/zombies/barricades/handle_repair with storage mgs:temp _brptick
execute if score @s mgs.zb.barricade.rp_timer matches 0 if score @s mgs.zb.barricade.state matches 1 run function mgs:v5.1.0/zombies/barricades/find_repairer with storage mgs:temp _brptick

