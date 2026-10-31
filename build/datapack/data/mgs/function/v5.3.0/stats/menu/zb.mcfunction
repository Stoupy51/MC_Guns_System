
#> mgs:v5.3.0/stats/menu/zb
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/menu/view
#

data modify storage mgs:temp _sv.d set from storage mgs:temp _sv.p.zb
data modify storage mgs:temp _sv.d.name set from storage mgs:temp _sv.p.name
data modify storage mgs:temp _sv.d.i set from storage mgs:temp _sv.i
execute store result storage mgs:temp _sv.d.points_spent int 100 run data get storage mgs:temp _sv.d.points_spent
execute store result score #st_t mgs.data run data get storage mgs:temp _sv.d.time
scoreboard players operation #st_t mgs.data /= #60 mgs.data
scoreboard players operation #st_n mgs.data = #st_t mgs.data
execute store result storage mgs:temp _sv.d.time_h int 1 run scoreboard players operation #st_n mgs.data /= #60 mgs.data
execute store result storage mgs:temp _sv.d.time_m int 1 run scoreboard players operation #st_t mgs.data %= #60 mgs.data
function mgs:v5.3.0/stats/menu/zb_dialog with storage mgs:temp _sv.d

