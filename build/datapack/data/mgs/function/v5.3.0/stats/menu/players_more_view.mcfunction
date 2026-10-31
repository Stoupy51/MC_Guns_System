
#> mgs:v5.3.0/stats/menu/players_more_view
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/menu/players_list with storage mgs:temp _sp
#
# @args		page_trigger (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.next_page",fallback:"Next page",color:"aqua"},action:{type:"run_command",command:"/trigger mgs.player.config set $(page_trigger)"}}

