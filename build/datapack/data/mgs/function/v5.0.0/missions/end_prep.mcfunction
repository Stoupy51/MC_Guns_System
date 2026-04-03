
#> mgs:v5.0.0/missions/end_prep
#
# @within	mgs:v5.0.0/missions/preload_complete 180t [ scheduled ]
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

# Spawn all enemies from map data
function mgs:v5.0.0/missions/spawn_all_enemies

# Run map-defined start commands after enemies are spawned
execute if data storage mgs:missions game.map.start_commands[0] run function mgs:v5.0.0/shared/run_start_commands {mode:"missions"}

# Give compass pointing to nearest enemy (hotbar slot 3)
execute as @a[scores={mgs.mi.in_game=1}] run item replace entity @s hotbar.3 with compass[custom_data={mgs:{compass:true}}]

# Reset mission timer (counts up)
scoreboard players set #mi_timer mgs.data 0

# Announce
tellraw @a ["",{"text":"","color":"aqua","bold":true},"🎯 ",{"translate":"mgs.go_go_go_kill_all_enemies"}]

