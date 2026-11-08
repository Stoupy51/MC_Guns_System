
#> mgs:v5.4.1/stats/menu/mi_tabs
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/stats/menu/mi_dialog with storage mgs:temp _sv.t
#
# @args		trigger_zb (unknown)
#			trigger_mp (unknown)
#			trigger_mi (unknown)
#

$data modify storage mgs:temp dialog.body prepend value {type:"minecraft:plain_message",width:300,contents:["",[{"text": "[", "color": "gray", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set $(trigger_zb)"}}, "Zombies", "]"],"  ",[{"text": "[", "color": "gray", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set $(trigger_mp)"}}, "Multiplayer", "]"],"  ",[{"text": "[", "color": "gold", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set $(trigger_mi)"}}, "Missions", "]"],"  ",[{"text": "[", "color": "yellow", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 90000"}}, "Players", "]"],"  ",[{"text": "[", "color": "aqua", "click_event": {"action": "run_command", "command": "/trigger mgs.player.config set 1"}}, "Settings", "]"]]}

