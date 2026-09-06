
#> mgs:v5.1.0/zombies/zombie_finish_rise
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/zombie_rise_tick
#

data modify entity @s NoAI set value 0b
tag @s remove mgs.zb_rising

# Safety net for the horde alliance (escort.py): summon_zombie_at already joins, but a zombie that
# somehow missed it makes every escort trader within 8 blocks flee it at 0.5 instead of walking at
# 0.35. One command, once per zombie, on a sweep that is already iterating it.
team join mgs.horde @s

# Walk-to spawn: hand it to an escort taxi that walks it to the map maker's spot. Only now that the
# rise is over — the escort freezes the zombie, which would strand it mid-animation.
execute if data entity @s data.walk_to run function mgs:v5.1.0/zombies/escort/start_to_target

## sourceMappingURL=zombie_finish_rise.mcfunction.map
