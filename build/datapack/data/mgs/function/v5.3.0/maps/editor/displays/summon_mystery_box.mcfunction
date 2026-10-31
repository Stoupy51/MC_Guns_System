
#> mgs:v5.3.0/maps/editor/displays/summon_mystery_box
#
# @executed	at @s
#
# @within	mgs:v5.3.0/maps/editor/displays/turn_mystery_box
#

execute if score @s mgs.mb.roll matches 0 run execute positioned ~ ~0.5 ~ positioned ^ ^0.6 ^0.3 run function mgs:v5.3.0/maps/editor/displays/mystery_box_parts
execute if score @s mgs.mb.roll matches 1 run execute positioned ~ ~0.5 ~ positioned ^-0.6 ^ ^0.3 run function mgs:v5.3.0/maps/editor/displays/mystery_box_parts
execute if score @s mgs.mb.roll matches 2 run execute positioned ~ ~0.5 ~ positioned ^ ^-0.6 ^0.3 run function mgs:v5.3.0/maps/editor/displays/mystery_box_parts
execute if score @s mgs.mb.roll matches 3 run execute positioned ~ ~0.5 ~ positioned ^0.6 ^ ^0.3 run function mgs:v5.3.0/maps/editor/displays/mystery_box_parts

