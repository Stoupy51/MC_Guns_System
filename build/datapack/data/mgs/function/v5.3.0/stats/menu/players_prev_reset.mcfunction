
#> mgs:v5.3.0/stats/menu/players_prev_reset
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/menu/players_list with storage mgs:temp _sp
#
# @args		page (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.previous_page",fallback:"Previous page",color:"aqua"},action:{type:"run_command",command:"/function mgs:v5.3.0/stats/admin/players {page:$(page)}"}}

