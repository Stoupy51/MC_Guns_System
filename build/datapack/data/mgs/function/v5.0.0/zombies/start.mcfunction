
#> mgs:v5.0.0/zombies/start
#
# @within	mgs:v5.0.0/zombies/setup "hover_event": {"action": "show_text", "value": "Start the zombies game"}}, "\u25b6 START", "]"]," ",[{"text": "[", "color": "red", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/zombies/stop"}, "hover_event": {"action": "show_text", "value": "Stop the zombies game"}}, "\u25a0 STOP", "]"]," ",[{"text": "[", "color": "dark_aqua", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/multiplayer/show_teams"}, "hover_event": {"action": "show_text", "value": "Show which players have team assignments"}}, "\ud83d\udc65 Roster", "]"]," ",[{"text": "[", "color": "yellow", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/zombies/join_game"}, "hover_event": {"action": "show_text", "value": "Join the ongoing zombies game as a late joiner"}}, "+ Join", "]"]]
#

# Prevent starting if already active or preparing
execute if data storage mgs:zombies game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.zombies_game_already_in_progress","color":"red"}]
execute if data storage mgs:zombies game{state:"preparing"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.zombies_game_already_preparing","color":"red"}]

# Check that a map is selected
execute unless data storage mgs:zombies game.map_id run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_map_selected_use_the_setup_menu_to_select_a_zombies_map","color":"red"}]
execute if data storage mgs:zombies game{map_id:""} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_map_selected_use_the_setup_menu_to_select_a_zombies_map","color":"red"}]

# Load the selected map
function mgs:v5.0.0/zombies/load_map_from_storage with storage mgs:zombies game
execute unless score #map_load_found mgs.data matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.map_not_found_select_a_valid_zombies_map","color":"red"}]

# Copy loaded map data into game state
data modify storage mgs:zombies game.map set from storage mgs:temp map_load.result

# Set state to preparing
data modify storage mgs:zombies game.state set value "preparing"

# Reset scores
scoreboard players set @a mgs.zb.in_game 0
scoreboard players set @a mgs.zb.points 500
scoreboard players set @a mgs.zb.kills 0
scoreboard players set @a mgs.zb.downs 0
scoreboard players set @a mgs.zb.passive 0
scoreboard players set @a mgs.zb.ability 0
scoreboard players set @a mgs.zb.ability_cd 0

# Tag all players as in-game
scoreboard players set @a mgs.zb.in_game 1

# Initialize kill tracking baseline (so kills before game start don't count)
execute as @a run scoreboard players operation @s mgs.zb.prev_kills = @s mgs.total_kills

# Reset death counters and spectate timers to prevent false triggers
scoreboard players set @a mgs.mp.death_count 0
scoreboard players set @a mgs.mp.spectate_timer 0

# Disable natural regeneration, enable custom regen system
# Disable natural regeneration, enable custom regen system
gamerule natural_health_regeneration false
scoreboard players set #any_game_active mgs.data 1

# Reset per-player regen state
scoreboard players set @a mgs.last_hit 0
execute as @a run execute store result score @s mgs.hp_prev run data get entity @s Health 1

# Set gamerules
gamemode spectator @a[scores={mgs.zb.in_game=1}]
gamerule immediate_respawn true
gamerule keep_inventory true
gamerule max_entity_cramming 96

# Initialize round to 0 (first round will be 1)
data modify storage mgs:zombies game.round set value 0

# Store base coordinates for offset
function mgs:v5.0.0/shared/load_base_coordinates {mode:"zombies"}

# Check if map has boundaries defined
scoreboard players set #zb_has_bounds mgs.data 0
execute if data storage mgs:zombies game.map.boundaries[0] run scoreboard players set #zb_has_bounds mgs.data 1

# Normalize and store boundaries (only if defined)
execute if score #zb_has_bounds mgs.data matches 1 run function mgs:v5.0.0/shared/load_bounds {mode:"zombies"}

# Forceload the area (only if bounds defined)
execute if score #zb_has_bounds mgs.data matches 1 run function mgs:v5.0.0/shared/forceload_area

# Teleport all players as spectator to base coordinates for chunk preloading
execute store result storage mgs:temp _tp.x int 1 run scoreboard players get #gm_base_x mgs.data
execute store result storage mgs:temp _tp.y int 1 run scoreboard players get #gm_base_y mgs.data
execute store result storage mgs:temp _tp.z int 1 run scoreboard players get #gm_base_z mgs.data
execute as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.0.0/shared/tp_to_position with storage mgs:temp _tp

# Register custom maps and mystery box items (extension points)
function #mgs:zombies/register_maps
function #mgs:zombies/register_mystery_box_item

# Schedule preload completion after 1 second
schedule function mgs:v5.0.0/zombies/preload_complete 20t

# Announce
tellraw @a ["",{"text":"","color":"dark_green","bold":true},"🧟 ",{"translate":"mgs.loading_zombies_map","color":"yellow"}]

# Initialize power state
scoreboard players set #zb_power mgs.data 0

# Initialize unlocked groups (group 0 = starting area, compound keys for quick lookup)
data modify storage mgs:zombies game.unlocked_groups set value {"0": 1b}

# Reset perk scoreboards for all known score holders (including offline players).
scoreboard players reset * mgs.zb.perk.juggernog
scoreboard players reset * mgs.zb.perk.speed_cola
scoreboard players reset * mgs.zb.perk.double_tap
scoreboard players reset * mgs.zb.perk.quick_revive
scoreboard players reset * mgs.zb.perk.mule_kick

# Reset revive state
scoreboard players set @a mgs.zb.downed 0
scoreboard players set @a mgs.zb.bleed 0
scoreboard players set @a mgs.zb.revive_p 0
scoreboard players set @a mgs.zb.qr_uses 0
scoreboard players set @a mgs.zb.downed_id 0
scoreboard players set #downed_id_next mgs.data 0
tag @a remove mgs.downed_spectator
kill @e[tag=mgs.downed_mannequin]
kill @e[tag=mgs.downed_hud]
kill @e[tag=mgs.downed_cam]

