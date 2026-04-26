
#> mgs:v5.0.0/zombies/zombie_rise_tick
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/game_tick [ at @s ]
#

# Rise 0.1 blocks per tick
tp @s ~ ~0.1 ~

# Emit block-breaking particles from the block at the surface (2 blocks above spawn = ~0 now that we're rising)
# Read the block type at +2 above original spawn (approximately ground level)
execute positioned ~ ~ ~ run function #bs.block:get_type
data modify storage mgs:temp _rise_particle.block set from storage bs:out block.type
function mgs:v5.0.0/zombies/zombie_rise_particles with storage mgs:temp _rise_particle

# Count down rise timer
scoreboard players remove @s mgs.zb.rise_tick 1
execute if score @s mgs.zb.rise_tick matches ..0 run function mgs:v5.0.0/zombies/zombie_finish_rise

