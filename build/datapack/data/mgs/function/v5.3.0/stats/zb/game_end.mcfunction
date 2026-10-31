
#> mgs:v5.3.0/stats/zb/game_end
#
# @within	mgs:v5.3.0/stats/zb/on_game_end
#

data modify storage mgs:temp _st_roster set from storage mgs:stats rosters.zb
execute store result score #lb_n mgs.data run data get storage mgs:temp _st_roster
data modify storage mgs:temp _st_map set from storage mgs:zombies game.map_id
function mgs:v5.3.0/stats/snapshot/roster_next {mode:"zb"}
function mgs:v5.3.0/stats/board/refresh_holograms

data remove storage mgs:stats rosters.zb
scoreboard players add #st_zb_game mgs.data 1

