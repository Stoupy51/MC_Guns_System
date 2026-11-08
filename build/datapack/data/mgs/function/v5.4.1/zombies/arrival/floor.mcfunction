
#> mgs:v5.4.1/zombies/arrival/floor
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/do_spawn
#

scoreboard players set #zb_rise_step mgs.data 2000
scoreboard players operation #zb_rise_step mgs.data /= @s mgs.zb.rise_tick
data modify storage mgs:temp _mob.no_ai set value 1b
execute positioned ~ ~-1.8 ~ run function mgs:v5.4.1/zombies/mob/spawn
function mgs:v5.4.1/zombies/arrival/rise
function mgs:v5.4.1/zombies/summon_rise_dust {block_y:"-1"}

