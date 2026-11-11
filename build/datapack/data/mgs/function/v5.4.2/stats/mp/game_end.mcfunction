
#> mgs:v5.4.2/stats/mp/game_end
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/stats/mp/on_game_end
#

data modify storage mgs:temp _st_roster set from storage mgs:stats rosters.mp
execute store result score #lb_n mgs.data run data get storage mgs:temp _st_roster
data modify storage mgs:temp _st_map set from storage mgs:multiplayer game.map_id
function mgs:v5.4.2/stats/snapshot/roster_next {mode:"mp"}
function mgs:v5.4.2/stats/board/refresh_holograms

data remove storage mgs:stats rosters.mp
scoreboard players add #st_mp_game mgs.data 1

