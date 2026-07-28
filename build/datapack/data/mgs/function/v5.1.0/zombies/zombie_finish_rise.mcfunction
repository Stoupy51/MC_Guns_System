
#> mgs:v5.1.0/zombies/zombie_finish_rise
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/zombie_rise_tick
#

data modify entity @s NoAI set value 0b
tag @s remove mgs.zb_rising

# Walk-to spawn: hand it to an escort taxi that walks it to the map maker's spot. Only now that the
# rise is over — the escort freezes the zombie, which would strand it mid-animation.
execute if data entity @s data.walk_to run function mgs:v5.1.0/zombies/escort/start_to_target

