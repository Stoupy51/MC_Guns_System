
#> mgs:v5.1.0/zombies/revive/set_hud_name
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/revive/spawn_downed_body with storage mgs:temp
#
# @args		rv_name (unknown)
#

$data modify entity @n[tag=mgs.downed_hud_new] text set value [{"text":"$(rv_name)","color":"yellow"},{"text":" ↓","color":"yellow"}]

