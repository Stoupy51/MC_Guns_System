
#> mgs:v5.4.2/zombies/zombie_finish_rise
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/zombie_rise_tick
#

data modify entity @s NoAI set value 0b
tag @s remove mgs.zb_rising

# The stuck timeout counts from here, so a long rise does not eat into it.
scoreboard players operation @s mgs.zb.stuck_ticks = #total_tick mgs.data

# The build already joins the horde; an enemy that missed it would make escort traders flee it.
team join mgs.horde @s

# Walk-to spawn: only once the rise is over, since the escort freezes the enemy.
execute if data entity @s data.walk_to run function mgs:v5.4.2/zombies/escort/start_to_target

