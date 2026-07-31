
#> mgs:v5.1.0/multiplayer/gamemodes/demo/set_site_hud
#
# @executed	as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/site_hud with storage mgs:temp _demo_hud
#
# @args		sec (unknown)
#

$data modify entity @n[tag=mgs.demo_bomb_hud,distance=..2] text set value [{"text":"💣 ","color":"red","bold":true},{"text":"$(sec)s","color":"white"}]

