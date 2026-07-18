
#> mgs:v5.1.0/multiplayer/gamemodes/hp/load_zone
#
# @executed	"","\ud83c\udfc6 ",{"translate":"mgs.score_limit"}],"tooltip":{"translate":"mgs.set_the_score_needed_to_win"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/dialogs/multiplayer/setup/score_limit"}},{"label":["","\u23f1 ",{"translate":"mgs.time_limit"}],"tooltip":{"translate":"mgs.set_the_match_time_limit"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/dialogs/multiplayer/setup/time_limit"}},{"label":["","\ud83d\uddfa ",{"translate":"mgs.select_map","color":"aqua"}],"tooltip":{"translate":"mgs.browse_and_select_a_map"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/map_select"}},{"label":["","\u25b6 ",{"translate":"mgs.start","color":"green"}],"tooltip":{"translate":"mgs.start_the_match"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/start"}},{"label":["","\u25a0 ",{"translate":"mgs.stop","color":"red"}],"tooltip":{"translate":"mgs.stop_the_match"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/stop"}},{"label":["","\u2694 ",{"translate":"mgs.classes","color":"aqua"}],"tooltip":{"translate":"mgs.select_your_class"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/select_class"}},{"label":["","+ ",{"translate":"mgs.join","color":"yellow"}],"tooltip":{"translate":"mgs.join_the_ongoing_game_as_a_late_joiner"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/join_game"}},{"label":{"translate":"mgs.red_team","color":"red"},"tooltip":{"translate":"mgs.join_red_team"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/join_red"}},{"label":{"translate":"mgs.blue_team","color":"blue"},"tooltip":{"translate":"mgs.join_blue_team"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/join_blue"}},{"label":{"translate":"mgs.auto_team","color":"yellow"},"tooltip":{"translate":"mgs.auto_balance_across_red_blue_in_ffa_seats_everyone_on_the_single"},"action":{"type":"run_command","command":"/execute as @a[sort=random] run function mgs:v5.1.0/multiplayer/auto_assign_team"}},{"label":["","\ud83d\udc65 ",{"translate":"mgs.manage_players","color":"dark_aqua"}],"tooltip":{"translate":"mgs.assign_players_to_red_blue_teams"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/players/list_multiplayer"}}],"columns":2,"exit_action":{"label":["","\u25c0 ",{"translate":"mgs.back","color":"gray"}
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/hp/setup
#			mgs:v5.1.0/multiplayer/gamemodes/hp/rotate
#

# Kill old zone marker
kill @e[tag=mgs.hp_marker]
kill @e[tag=mgs.hp_label]

# Zone point: relative → absolute
execute store result score #rx mgs.data run data get storage mgs:multiplayer game.hp_zones[0][0]
execute store result score #ry mgs.data run data get storage mgs:multiplayer game.hp_zones[0][1]
execute store result score #rz mgs.data run data get storage mgs:multiplayer game.hp_zones[0][2]
scoreboard players operation #rx mgs.data += #gm_base_x mgs.data
scoreboard players operation #ry mgs.data += #gm_base_y mgs.data
scoreboard players operation #rz mgs.data += #gm_base_z mgs.data
execute store result storage mgs:temp _hp_pos.x double 1 run scoreboard players get #rx mgs.data
execute store result storage mgs:temp _hp_pos.y double 1 run scoreboard players get #ry mgs.data
execute store result storage mgs:temp _hp_pos.z double 1 run scoreboard players get #rz mgs.data

# Assign point label (fallback to HP for maps with >5 zones)
data modify storage mgs:temp _hp_pos.label set value "HP"
execute if score #hp_zone_idx mgs.data matches 0 run data modify storage mgs:temp _hp_pos.label set value "A"
execute if score #hp_zone_idx mgs.data matches 1 run data modify storage mgs:temp _hp_pos.label set value "B"
execute if score #hp_zone_idx mgs.data matches 2 run data modify storage mgs:temp _hp_pos.label set value "C"
execute if score #hp_zone_idx mgs.data matches 3 run data modify storage mgs:temp _hp_pos.label set value "D"
execute if score #hp_zone_idx mgs.data matches 4 run data modify storage mgs:temp _hp_pos.label set value "E"
scoreboard players add #hp_zone_idx mgs.data 1

function mgs:v5.1.0/multiplayer/gamemodes/hp/summon_marker with storage mgs:temp _hp_pos

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"⚡ ",{"translate":"mgs.hardpoint_2","color":"dark_purple"},{"storage":"mgs:temp","nbt":"_hp_pos.label","color":"yellow","interpret":true},[{"text":" ","color":"dark_purple"}, {"translate":"mgs.active"}]]
playsound minecraft:block.note_block.chime player @a ~ ~ ~ 1 1.0

