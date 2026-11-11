
#> mgs:v5.4.2/stats/board/filters_add
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/stats/board/filters with storage mgs:temp _lb_view
#
# @args		f0 (unknown)
#			f1 (unknown)
#			f2 (unknown)
#			f3 (unknown)
#			f4 (unknown)
#

$data modify storage mgs:temp dialog.body[0].contents append value [[{"text": "[", "color": "aqua", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set $(f0)"}}, "All", "]"],"  "]
$data modify storage mgs:temp dialog.body[0].contents append value [[{"text": "[", "color": "aqua", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set $(f1)"}}, "1 player", "]"],"  "]
$data modify storage mgs:temp dialog.body[0].contents append value [[{"text": "[", "color": "aqua", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set $(f2)"}}, "2 players", "]"],"  "]
$data modify storage mgs:temp dialog.body[0].contents append value [[{"text": "[", "color": "aqua", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set $(f3)"}}, "3 players", "]"],"  "]
$data modify storage mgs:temp dialog.body[0].contents append value [[{"text": "[", "color": "aqua", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set $(f4)"}}, "4 players", "]"],"  "]

