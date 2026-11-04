
#> mgs:v5.3.0/zombies/revive/set_hud_name
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zombies/revive/spawn_downed_body with storage mgs:temp
#
# @args		rv_name (unknown)
#

$data modify entity @n[tag=mgs.downed_hud_new] text set value [{"text":"$(rv_name)","color":"yellow"},{"text":" ↓","color":"yellow"}]

