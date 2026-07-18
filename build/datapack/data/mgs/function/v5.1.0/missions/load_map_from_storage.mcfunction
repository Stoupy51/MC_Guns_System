
#> mgs:v5.1.0/missions/load_map_from_storage
#
# @executed	"","\u25b6 ",{"translate":"mgs.start","color":"green"}],"tooltip":{"translate":"mgs.start_the_mission"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/missions/start"}},{"label":["","\u25a0 ",{"translate":"mgs.stop","color":"red"}],"tooltip":{"translate":"mgs.stop_the_mission"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/missions/stop"}},{"label":["","\u2694 ",{"translate":"mgs.classes","color":"aqua"}],"tooltip":{"translate":"mgs.select_your_class"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/select_class"}},{"label":["","\ud83d\udc65 ",{"translate":"mgs.manage_players","color":"dark_aqua"}],"tooltip":{"translate":"mgs.add_or_remove_players_from_the_mission"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/players/list_missions"}},{"label":["","\ud83d\udc65 ",{"translate":"mgs.all_players_join","color":"green"}],"tooltip":{"translate":"mgs.add_every_online_player_to_the_mission"},"action":{"type":"run_command","command":"/execute as @a run function mgs:v5.1.0/players/mi_join"}},{"label":["","+ ",{"translate":"mgs.join","color":"yellow"}],"tooltip":{"translate":"mgs.join_the_ongoing_mission_as_a_late_joiner"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/missions/join_game"}}
#
# @within	mgs:v5.1.0/missions/start with storage mgs:missions game
#
# @args		map_id (unknown)
#

$function mgs:v5.1.0/shared/maps/load {id:"$(map_id)",mode:"missions",override:{}}

