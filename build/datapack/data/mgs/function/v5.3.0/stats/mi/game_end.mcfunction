
#> mgs:v5.3.0/stats/mi/game_end
#
# @within	mgs:v5.3.0/stats/mi/on_mission_end
#

data modify storage mgs:temp _st_roster set from storage mgs:stats rosters.mi
execute store result score #lb_n mgs.data run data get storage mgs:temp _st_roster
data modify storage mgs:temp _st_map set from storage mgs:missions game.map_id
function mgs:v5.3.0/stats/snapshot/roster_next {mode:"mi"}
function mgs:v5.3.0/stats/board/refresh_holograms

data remove storage mgs:stats rosters.mi
scoreboard players add #st_mi_game mgs.data 1

