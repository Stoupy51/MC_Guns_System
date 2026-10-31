
#> mgs:v5.3.0/stats/admin/players
#
# @executed	as the player & at current position
#
# @within	string in mgs:v5.3.0/stats/menu/players_prev_reset {page:$(page)}
#			string in mgs:v5.3.0/stats/menu/players_more_reset {page:$(page)}
#			dialog mgs:v5.3.0/config
#
# @args		page (unknown)
#

$scoreboard players set #st_page mgs.data $(page)
function mgs:v5.3.0/stats/menu/players_list {kind:"reset",title:"Reset Player Stats"}

