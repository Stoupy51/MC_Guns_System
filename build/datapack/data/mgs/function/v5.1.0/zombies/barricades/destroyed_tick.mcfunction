
#> mgs:v5.1.0/zombies/barricades/destroyed_tick
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/barricades/tick
#			mgs:v5.1.0/zombies/barricades/destroyed_tick [ positioned ~ ~-1 ~ ]
#

# Upper barricades of a column share the floor-level detection, so a player on the ground can repair them.
execute positioned ~ ~-1 ~ if block ~ ~ ~ air run return run function mgs:v5.1.0/zombies/barricades/destroyed_tick

# Run as the destroyed barricade display, at it.
execute store result score #barricade_id mgs.data run scoreboard players get @s mgs.zb.barricade.id
execute store result storage mgs:temp _brptick.radius int 1 run scoreboard players get @s mgs.zb.barricade.radius

execute if score @s mgs.zb.barricade.rp_timer matches 1.. run function mgs:v5.1.0/zombies/barricades/handle_repair with storage mgs:temp _brptick
execute if score @s mgs.zb.barricade.rp_timer matches 0 if score @s mgs.zb.barricade.state matches 1 run function mgs:v5.1.0/zombies/barricades/find_repairer with storage mgs:temp _brptick

