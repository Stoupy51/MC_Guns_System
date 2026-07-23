
#> mgs:v5.1.0/zombies/whos_who/tp_body
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/whos_who/on_down with storage mgs:temp
#
# @args		rv_x (unknown)
#			rv_y (unknown)
#			rv_z (unknown)
#

$tp @n[tag=mgs.ww_body_new] $(rv_x) $(rv_y) $(rv_z)
$tp @n[tag=mgs.ww_hud_new] $(rv_x) $(rv_y) $(rv_z)
tp @n[tag=mgs.ww_hud_new] ~ ~2 ~

