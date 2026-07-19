
#> mgs:v5.1.0/missions/stop
#
# @within	mgs:v5.1.0/missions/end_prep
#			mgs:v5.1.0/missions/victory
#

# Various cleanup and reset tasks to return to lobby state
data modify storage mgs:missions game.state set value "lobby"
schedule clear mgs:v5.1.0/missions/end_prep
execute as @a[scores={mgs.mi.in_game=1}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={mgs.mi.in_game=1}] run attribute @s minecraft:jump_strength base reset
effect clear @a[scores={mgs.mi.in_game=1}] darkness
effect clear @a[scores={mgs.mi.in_game=1}] blindness
effect clear @a[scores={mgs.mi.in_game=1}] night_vision
gamemode adventure @a[scores={mgs.mi.in_game=1},gamemode=spectator]
clear @a[scores={mgs.mi.in_game=1}] compass[custom_data~{mgs:{compass:true}}]

kill @e[tag=mgs.mission_enemy]
kill @e[tag=mgs.gm_entity]

# Remove forceload
execute if score #mi_has_boundary mgs.data matches 1 run function mgs:v5.1.0/shared/remove_forceload

# Signal mission end
function #mgs:missions/on_mission_end

# Re-enable natural regeneration, disable custom regen system
gamerule natural_health_regeneration true
scoreboard players set #any_game_active mgs.data 0

# Tear down stamina state: stop any hunger drain and refill the bar so nobody is left winded
effect clear @a minecraft:hunger
effect give @a minecraft:saturation 5 20 true
scoreboard players set @a mgs.stam_out 0
scoreboard players set @a mgs.stam_seen 0

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.mission_ended","color":"red"}]

execute as @a[scores={mgs.mi.in_game=1}] run function mgs:v5.1.0/shared/maps/call_leave_script_at_base

# Reset in-game state
scoreboard players set @a[scores={mgs.mi.in_game=1}] mgs.mp.team 0
scoreboard players set @a mgs.mi.in_game 0
scoreboard players set #mi_timer mgs.data 0
scoreboard players set #mi_total_enemies mgs.data 0
scoreboard players set #mi_has_boundary mgs.data 0
scoreboard players set @a mgs.mi.kills 0
scoreboard players set @a mgs.mi.deaths 0
tag @a[tag=mgs.give_class_menu] remove mgs.give_class_menu

