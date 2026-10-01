
#> mgs:v5.1.0/missions/preload_complete
#
# @within	mgs:v5.1.0/missions/start 20t [ scheduled ]
#

execute unless data storage mgs:missions game{state:"preparing"} run return fail

gamemode adventure @a[scores={mgs.mi.in_game=1}]

function mgs:v5.1.0/shared/summon_oob {mode:"missions"}

function mgs:v5.1.0/missions/summon_spawns

function #mgs:missions/on_mission_start

function mgs:v5.1.0/missions/tp_all_to_spawns

effect give @a[scores={mgs.mi.in_game=1}] darkness 25 255 true
effect give @a[scores={mgs.mi.in_game=1}] blindness 25 255 true
effect give @a[scores={mgs.mi.in_game=1}] night_vision 25 255 true
execute as @a[scores={mgs.mi.in_game=1}] run attribute @s minecraft:movement_speed base set 0
execute as @a[scores={mgs.mi.in_game=1}] run attribute @s minecraft:jump_strength base set 0
execute as @a[scores={mgs.mi.in_game=1}] run attribute @s minecraft:waypoint_receive_range base reset

execute as @a[scores={mgs.mi.in_game=1}] at @s unless score @s mgs.mp.class matches 0 run function mgs:v5.1.0/multiplayer/apply_class

# `add 0` initializes unset scores, so the `matches 0` test below can succeed.
scoreboard players add @a mgs.mp.class 0
execute as @a[scores={mgs.mi.in_game=1}] at @s if score @s mgs.mp.class matches 0 if score @s mgs.mp.default matches 1.. run function mgs:v5.1.0/multiplayer/auto_apply_default

execute as @a[scores={mgs.mi.in_game=1}] run function mgs:v5.1.0/multiplayer/select_class

# For change detection during prep.
execute as @a[scores={mgs.mi.in_game=1}] run scoreboard players operation @s mgs.mp.prev_class = @s mgs.mp.class

# Prep lasts 9 s.
schedule function mgs:v5.1.0/missions/end_prep 180t

tellraw @a ["",{"text":"","color":"aqua","bold":true},"🎯 ",{"translate":"mgs.preparing_choose_your_class_mission_starts_in_9_seconds","color":"yellow"}]

