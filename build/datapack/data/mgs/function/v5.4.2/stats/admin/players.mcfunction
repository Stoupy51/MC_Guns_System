
#> mgs:v5.4.2/stats/admin/players
#
# @within	mgs:v5.4.2/dialog/close_then
#			string in mgs:v5.4.2/stats/menu/players_prev_reset {page:$(page)}
#			string in mgs:v5.4.2/stats/menu/players_more_reset {page:$(page)}
#			dialog mgs:v5.4.2/config
#
# @args		page (unknown)
#

$scoreboard players set #st_page mgs.data $(page)
function mgs:v5.4.2/stats/menu/players_list {kind:"reset",title:"Reset Player Stats"}

