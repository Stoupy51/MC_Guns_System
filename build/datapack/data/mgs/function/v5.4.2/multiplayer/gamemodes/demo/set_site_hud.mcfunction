
#> mgs:v5.4.2/multiplayer/gamemodes/demo/set_site_hud
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/gamemodes/demo/site_hud with storage mgs:temp _demo_hud
#
# @args		sec (unknown)
#

$data modify entity @n[tag=mgs.demo_bomb_hud,distance=..2] text set value [{"text":"💣 ","color":"white"},{"text":"$(sec)s","color":"white","bold":true}]

