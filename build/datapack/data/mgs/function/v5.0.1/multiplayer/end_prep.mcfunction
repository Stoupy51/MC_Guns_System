
#> mgs:v5.0.1/multiplayer/end_prep
#
# @within	mgs:v5.0.1/multiplayer/start 200t [ scheduled ]
#

execute unless data storage mgs:multiplayer game{state:"preparing"} run return fail
data modify storage mgs:multiplayer game.state set value "active"
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:jump_strength base reset
effect clear @a[scores={mgs.mp.in_game=1}] darkness
effect clear @a[scores={mgs.mp.in_game=1}] blindness
effect clear @a[scores={mgs.mp.in_game=1}] night_vision
effect give @a[scores={mgs.mp.in_game=1}] saturation infinite 255 true

# Call map start scripts (state is now active, chunks had time to load)
function mgs:v5.0.1/shared/maps/call_start_script_at_base

# Announce
tellraw @a [{"text":"","color":"green","bold":true},"⚔ ",{"translate":"mgs.go_go_go"}]

