
#> mgs:v5.1.0/missions/end_prep
#
# @within	mgs:v5.1.0/missions/preload_complete 180t [ scheduled ]
#

execute unless data storage mgs:missions game{state:"preparing"} run return fail
data modify storage mgs:missions game.state set value "active"
execute as @a[scores={mgs.mi.in_game=1}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={mgs.mi.in_game=1}] run attribute @s minecraft:jump_strength base reset
effect clear @a[scores={mgs.mi.in_game=1}] darkness
effect clear @a[scores={mgs.mi.in_game=1}] blindness
effect clear @a[scores={mgs.mi.in_game=1}] night_vision

# Spawn all enemies from map data
function mgs:v5.1.0/missions/spawn_all_enemies

# A mission with no enemies would instantly "complete" — abort instead (empty map or broken enemy functions)
execute if score #mi_total_enemies mgs.data matches ..0 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_enemies_could_be_spawned_check_the_maps_enemy_markers_functio","color":"red"}]
execute if score #mi_total_enemies mgs.data matches ..0 run return run function mgs:v5.1.0/missions/stop

# Run map-defined start commands after enemies are spawned
execute if data storage mgs:missions game.map.start_commands[0] run function mgs:v5.1.0/shared/run_start_commands {mode:"missions"}

# Call map start scripts (state is now active, chunks had time to load)
function mgs:v5.1.0/shared/maps/call_script_at_base {script:"start"}

# Give compass pointing to nearest enemy (hotbar slot 3)
execute as @a[scores={mgs.mi.in_game=1}] run item replace entity @s hotbar.3 with compass[custom_data={mgs:{compass:true}}]

# Reset mission timer (counts up)
scoreboard players set #mi_timer mgs.data 0

# Announce
tellraw @a ["",{"text":"","color":"aqua","bold":true},"🎯 ",{"translate":"mgs.go_go_go_kill_all_enemies"}]

