
#> mgs:v5.1.0/zombies/barricades/intact_tick
#
# @executed	positioned ^ ^ ^-1
#
# @within	mgs:v5.1.0/zombies/barricades/tick [ positioned ^ ^ ^-1 ]
#			mgs:v5.1.0/zombies/barricades/intact_tick [ positioned ~ ~-1 ~ ]
#

# Delegate detection downward if floating (upper barricades in a column share floor-level detection)
execute positioned ~ ~-1 ~ if block ~ ~ ~ air run return run function mgs:v5.1.0/zombies/barricades/intact_tick

# @s = intact barricade display, at @s
execute store result score #barricade_id mgs.data run scoreboard players get @s mgs.zb.barricade.id
execute store result storage mgs:temp _btick.radius int 1 run scoreboard players get @s mgs.zb.barricade.radius

# Freeze all zombies in radius (macro)
function mgs:v5.1.0/zombies/barricades/freeze_zombies with storage mgs:temp _btick

# Handle remove timer or find a new remover (both macros using radius)
execute if score @s mgs.zb.barricade.r_timer matches 1.. run function mgs:v5.1.0/zombies/barricades/handle_removing with storage mgs:temp _btick
execute if score @s mgs.zb.barricade.r_timer matches 0 if score @s mgs.zb.barricade.state matches 0 run function mgs:v5.1.0/zombies/barricades/find_remover with storage mgs:temp _btick

