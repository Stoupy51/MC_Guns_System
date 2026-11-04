
#> mgs:v5.3.0/stats/admin/reset_board
#
# @within	mgs:v5.3.0/dialog/close_then
#			string in mgs:v5.3.0/stats/board/admin_button {board:$(board),id:$(id)}
#
# @args		board (unknown)
#			id (unknown)
#

$data remove storage mgs:stats leaderboards.$(board)."$(id)"
function mgs:v5.3.0/stats/board/refresh_holograms
$tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"text":"Leaderboard reset: $(id)","color":"yellow"}]

