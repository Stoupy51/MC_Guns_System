
#> mgs:v5.3.0/zombies/arrival/ceiling
#
# @executed	at @s
#
# @within	mgs:v5.3.0/zombies/do_spawn
#

scoreboard players set #zb_rise_step mgs.data -2000
scoreboard players operation #zb_rise_step mgs.data /= @s mgs.zb.rise_tick
data modify storage mgs:temp _mob.no_ai set value 1b
execute positioned ~ ~2.2 ~ run function mgs:v5.3.0/zombies/mob/spawn
function mgs:v5.3.0/zombies/arrival/rise
execute positioned ~ ~2 ~ run function mgs:v5.3.0/zombies/summon_rise_dust {block_y:"0"}

