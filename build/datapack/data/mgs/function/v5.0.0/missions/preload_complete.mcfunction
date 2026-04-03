
#> mgs:v5.0.0/missions/preload_complete
#
# @within	mgs:v5.0.0/missions/start 20t [ scheduled ]
#

# Guard: only if still preparing
execute unless data storage mgs:missions game{state:"preparing"} run return fail

# Switch to adventure mode
gamemode adventure @a[scores={mgs.mi.in_game=1}]

# Summon OOB markers
function mgs:v5.0.0/shared/summon_oob {mode:"missions"}

# Summon spawn point markers
function mgs:v5.0.0/missions/summon_spawns

# Signal mission start
function #mgs:missions/on_mission_start

# Teleport all players to mission spawns
function mgs:v5.0.0/missions/tp_all_to_spawns

# Freeze players during prep
effect give @a[scores={mgs.mi.in_game=1}] darkness 25 255 true
effect give @a[scores={mgs.mi.in_game=1}] blindness 25 255 true
effect give @a[scores={mgs.mi.in_game=1}] night_vision 25 255 true
effect give @a[scores={mgs.mi.in_game=1}] saturation infinite 255 true
execute as @a[scores={mgs.mi.in_game=1}] run attribute @s minecraft:movement_speed base set 0
execute as @a[scores={mgs.mi.in_game=1}] run attribute @s minecraft:jump_strength base set 0
execute as @a[scores={mgs.mi.in_game=1}] run attribute @s minecraft:waypoint_receive_range base reset

# Give loadout to players who already have a class
execute as @a[scores={mgs.mi.in_game=1}] at @s unless score @s mgs.mp.class matches 0 run function mgs:v5.0.0/multiplayer/apply_class

# Auto-apply default custom loadout if no class set
scoreboard players add @s mgs.mp.class 0
execute as @a[scores={mgs.mi.in_game=1}] at @s if score @s mgs.mp.class matches 0 if score @s mgs.mp.default matches 1.. run function mgs:v5.0.0/multiplayer/auto_apply_default

# Show class selection
execute as @a[scores={mgs.mi.in_game=1}] run function mgs:v5.0.0/multiplayer/select_class

# Store current class for change detection
execute as @a[scores={mgs.mi.in_game=1}] run scoreboard players operation @s mgs.mp.prev_class = @s mgs.mp.class

# Schedule end of prep (9 seconds remaining)
schedule function mgs:v5.0.0/missions/end_prep 180t

# Announce
tellraw @a ["",{"text":"","color":"aqua","bold":true},"🎯 ",{"translate":"mgs.preparing_choose_your_class_mission_starts_in_9_seconds","color":"yellow"}]

