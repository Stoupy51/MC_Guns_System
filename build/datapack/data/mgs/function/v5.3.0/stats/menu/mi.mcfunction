
#> mgs:v5.3.0/stats/menu/mi
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/menu/view
#

data modify storage mgs:temp _sv.d set from storage mgs:temp _sv.p.mi
data modify storage mgs:temp _sv.d.name set from storage mgs:temp _sv.p.name
data modify storage mgs:temp _sv.d.i set from storage mgs:temp _sv.i
execute store result score #st_t mgs.data run data get storage mgs:temp _sv.d.time
scoreboard players operation #st_t mgs.data /= #60 mgs.data
scoreboard players operation #st_n mgs.data = #st_t mgs.data
execute store result storage mgs:temp _sv.d.time_h int 1 run scoreboard players operation #st_n mgs.data /= #60 mgs.data
execute store result storage mgs:temp _sv.d.time_m int 1 run scoreboard players operation #st_t mgs.data %= #60 mgs.data
execute store result score #st_n mgs.data run data get storage mgs:temp _sv.d.kills 10
execute store result score #st_d mgs.data run data get storage mgs:temp _sv.d.deaths
execute if score #st_d mgs.data matches 0 run scoreboard players set #st_d mgs.data 1
scoreboard players operation #st_n mgs.data /= #st_d mgs.data
scoreboard players operation #st_d mgs.data = #st_n mgs.data
execute store result storage mgs:temp _sv.d.kd_i int 1 run scoreboard players operation #st_n mgs.data /= #10 mgs.data
execute store result storage mgs:temp _sv.d.kd_d int 1 run scoreboard players operation #st_d mgs.data %= #10 mgs.data
function mgs:v5.3.0/stats/menu/mi_dialog with storage mgs:temp _sv.d

