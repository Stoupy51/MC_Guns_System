
#> mgs:v5.1.0/shared/forceload_remove
#
# @executed	"","\ud83e\uddec ",{"translate":"mgs.variant"}],"tooltip":{"translate":"mgs.choose_the_zombies_experience"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/dialogs/zombies/setup/variant"}},{"label":["","\u25b6 ",{"translate":"mgs.start","color":"green"}],"tooltip":{"translate":"mgs.start_the_zombies_game"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/zombies/start"}},{"label":["","\u25a0 ",{"translate":"mgs.stop","color":"red"}],"tooltip":{"translate":"mgs.stop_the_zombies_game"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/zombies/stop"}},{"label":["","\ud83d\udc65 ",{"translate":"mgs.manage_players","color":"dark_aqua"}],"tooltip":{"translate":"mgs.add_or_remove_players_from_the_zombies_game"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/players/list_zombies"}},{"label":["","\ud83d\udc65 ",{"translate":"mgs.all_players_join","color":"green"}],"tooltip":{"translate":"mgs.add_every_online_player_to_the_zombies_game"},"action":{"type":"run_command","command":"/execute as @a run function mgs:v5.1.0/players/zb_join"}},{"label":["","+ ",{"translate":"mgs.join","color":"yellow"}],"tooltip":{"translate":"mgs.join_the_ongoing_zombies_game_as_a_late_joiner"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/zombies/join_game"}}
#
# @within	mgs:v5.1.0/shared/remove_forceload with storage mgs:temp _fl
#
# @args		x1 (unknown)
#			z1 (unknown)
#			x2 (unknown)
#			z2 (unknown)
#

$forceload remove $(x1) $(z1) $(x2) $(z2)

