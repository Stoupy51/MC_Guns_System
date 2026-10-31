
#> mgs:v5.3.0/stats/board/maps_button
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/board/maps_next with storage mgs:temp _lb_maps[0]
#
# @args		name (unknown)
#			trigger (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{text:"$(name)",color:"yellow"},action:{type:"run_command",command:"/trigger mgs.player.config set $(trigger)"}}

