
#> mgs:v5.1.0/zombies/zombie_rise_tick
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/game_tick [ at @s ]
#

tp @s ~ ~0.1 ~

# Block particles from the surface, about 2 blocks above the spawn.
execute positioned ~ ~ ~ run function #bs.block:get_type
data modify storage mgs:temp _rise_particle.block set from storage bs:out block.type
function mgs:v5.1.0/zombies/zombie_rise_particles with storage mgs:temp _rise_particle

scoreboard players remove @s mgs.zb.rise_tick 1
execute if score @s mgs.zb.rise_tick matches ..0 run function mgs:v5.1.0/zombies/zombie_finish_rise

