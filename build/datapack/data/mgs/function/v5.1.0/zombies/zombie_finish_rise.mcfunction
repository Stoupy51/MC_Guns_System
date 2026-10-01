
#> mgs:v5.1.0/zombies/zombie_finish_rise
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/zombie_rise_tick
#

data modify entity @s NoAI set value 0b
tag @s remove mgs.zb_rising

# summon_zombie_at already joins the horde; a zombie that missed it would make escort traders flee it.
team join mgs.horde @s

# Walk-to spawn: only once the rise is over, since the escort freezes the zombie.
execute if data entity @s data.walk_to run function mgs:v5.1.0/zombies/escort/start_to_target

