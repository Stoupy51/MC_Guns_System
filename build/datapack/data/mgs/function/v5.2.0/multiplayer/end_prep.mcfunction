
#> mgs:v5.2.0/multiplayer/end_prep
#
# @within	mgs:v5.2.0/multiplayer/start 200t [ scheduled ]
#

execute unless score #in_multiplayer_map mgs.data matches 1 run return run function mgs:v5.2.0/shared/enter_map {mode:"multiplayer",fn:"mgs:v5.2.0/multiplayer/end_prep"}

execute unless data storage mgs:multiplayer game{state:"preparing"} run return fail
data modify storage mgs:multiplayer game.state set value "active"
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:jump_strength base reset
effect clear @a[scores={mgs.mp.in_game=1}] darkness
effect clear @a[scores={mgs.mp.in_game=1}] blindness
effect clear @a[scores={mgs.mp.in_game=1}] night_vision

# The state is now active and chunks had time to load.
function mgs:v5.2.0/shared/maps/call_script_at_base {mode:"multiplayer",script:"start"}

tellraw @a[scores={mgs.mp.in_game=1}] ["","⚔ ",[{"text":"","color":"green","bold":true},{"translate":"mgs.go_go_go","fallback":"GO! GO! GO!"}]]

