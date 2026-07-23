
#> mgs:v5.1.0/zombies/whos_who/set_hud_name
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/whos_who/on_down with storage mgs:temp
#
# @args		rv_name (unknown)
#

$data modify entity @n[tag=mgs.ww_hud_new] text set value [{"text":"$(rv_name)","color":"dark_aqua"},{"text":" ↓","color":"dark_aqua"}]

