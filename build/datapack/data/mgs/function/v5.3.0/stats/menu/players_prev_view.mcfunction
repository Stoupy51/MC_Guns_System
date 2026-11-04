
#> mgs:v5.3.0/stats/menu/players_prev_view
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/stats/menu/players_list with storage mgs:temp _sp
#
# @args		page_trigger (unknown)
#

$data modify storage mgs:temp dialog.body[0].contents append value ["  ",[{"text": "[", "color": "aqua", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set $(page_trigger)"}}, "Previous page", "]"]]

