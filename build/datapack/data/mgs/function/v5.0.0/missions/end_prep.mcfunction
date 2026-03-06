
#> mgs:v5.0.0/missions/end_prep
#
# @within	mgs:v5.0.0/missions/start 200t [ scheduled ]
#

# Guard: only if still preparing
execute unless data storage mgs:missions game{state:"preparing"} run return fail

# Transition to active
data modify storage mgs:missions game.state set value "active"

# Restore movement
execute as @a[scores={mgs.mi.in_game=1}] run attribute @s minecraft:movement_speed base set 0.1
execute as @a[scores={mgs.mi.in_game=1}] run attribute @s minecraft:jump_strength base set 0.42

# Clear prep effects
effect clear @a[scores={mgs.mi.in_game=1}] darkness
effect clear @a[scores={mgs.mi.in_game=1}] blindness
effect clear @a[scores={mgs.mi.in_game=1}] night_vision

# Keep saturation
effect give @a[scores={mgs.mi.in_game=1}] saturation infinite 255 true

# Announce
tellraw @a ["",{"text":"","color":"aqua","bold":true},"🎯 ",{"translate": "mgs.go_go_go"}]

# Start level 1
scoreboard players set #mi_level mgs.data 1
function mgs:v5.0.0/missions/spawn_level

