
#> mgs:v5.4.0/stats/menu/players_prev_reset
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/stats/menu/players_list with storage mgs:temp _sp
#
# @args		page (unknown)
#

$data modify storage mgs:temp dialog.body[0].contents append value ["  ",[{"text": "[", "color": "aqua", "click_event": {"action": "run_command", "command": "/function mgs:v5.4.0/stats/admin/players {page:$(page)}"}}, "Previous page", "]"]]

