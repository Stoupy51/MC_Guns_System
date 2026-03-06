
#> mgs:v5.0.0/missions/stop
#
# @within	mgs:v5.0.0/missions/victory
#

# Set state to lobby
data modify storage mgs:missions game.state set value "lobby"

# Cancel scheduled functions
schedule clear mgs:v5.0.0/missions/end_prep
schedule clear mgs:v5.0.0/missions/spawn_level

# Restore movement
execute as @a[scores={mgs.mi.in_game=1}] run attribute @s minecraft:movement_speed base set 0.1
execute as @a[scores={mgs.mi.in_game=1}] run attribute @s minecraft:jump_strength base set 0.42

# Clear effects
effect clear @a[scores={mgs.mi.in_game=1}] darkness
effect clear @a[scores={mgs.mi.in_game=1}] blindness
effect clear @a[scores={mgs.mi.in_game=1}] night_vision

# Kill all mission entities (enemies + markers)
kill @e[tag=mgs.mission_enemy]
kill @e[tag=mgs.gm_entity]

# Signal mission end
function #mgs:missions/on_mission_end

# Announce
tellraw @a [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.mission_ended","color":"red"}]

# Reset in-game state
scoreboard players set @a mgs.mi.in_game 0
scoreboard players set #mi_level mgs.data 0
tag @a[tag=mgs.give_class_menu] remove mgs.give_class_menu

