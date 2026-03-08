
#> mgs:v5.0.0/zombies/end_prep
#
# @within	mgs:v5.0.0/zombies/preload_complete 180t [ scheduled ]
#

# Guard: only if still preparing
execute unless data storage mgs:zombies game{state:"preparing"} run return fail

# Transition to active
data modify storage mgs:zombies game.state set value "active"

# Restore movement
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:movement_speed base set 0.1
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:jump_strength base set 0.42

# Clear prep effects
effect clear @a[scores={mgs.zb.in_game=1}] darkness
effect clear @a[scores={mgs.zb.in_game=1}] blindness
effect clear @a[scores={mgs.zb.in_game=1}] night_vision

# Keep saturation
effect give @a[scores={mgs.zb.in_game=1}] saturation infinite 255 true

# Start round 1
function mgs:v5.0.0/zombies/start_round

