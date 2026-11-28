
#> mgs:v5.4.4/stats/menu/zb
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/stats/menu/view
#

data modify storage mgs:temp _sv.d set value {games:0,rounds:0,best_round:0,kills:0,headshots:0,shots:0,hits:0,downs:0,deaths:0,revives:0,points_earned:0,points_spent:0,doors:0,boxes:0,wallbuys:0,perks:0,pap:0,traps:0,powerups:0,barricades:0,power:0,time:0}
data modify storage mgs:temp _sv.d merge from storage mgs:temp _sv.p.zb
data modify storage mgs:temp _sv.d.name set from storage mgs:temp _sv.p.name
data modify storage mgs:temp _sv.d.i set from storage mgs:temp _sv.i
execute store result storage mgs:temp _sv.d.points_spent int 100 run data get storage mgs:temp _sv.d.points_spent
execute store result score #st_t mgs.data run data get storage mgs:temp _sv.d.time
scoreboard players operation #st_t mgs.data /= #60 mgs.data
scoreboard players operation #st_n mgs.data = #st_t mgs.data
execute store result storage mgs:temp _sv.d.time_h int 1 run scoreboard players operation #st_n mgs.data /= #60 mgs.data
execute store result storage mgs:temp _sv.d.time_m int 1 run scoreboard players operation #st_t mgs.data %= #60 mgs.data
execute store result score #st_n mgs.data run data get storage mgs:temp _sv.d.hits 1000
execute store result score #st_d mgs.data run data get storage mgs:temp _sv.d.shots
execute if score #st_d mgs.data matches 0 run scoreboard players set #st_d mgs.data 1
scoreboard players operation #st_n mgs.data /= #st_d mgs.data
scoreboard players operation #st_d mgs.data = #st_n mgs.data
execute store result storage mgs:temp _sv.d.accuracy_i int 1 run scoreboard players operation #st_n mgs.data /= #10 mgs.data
execute store result storage mgs:temp _sv.d.accuracy_d int 1 run scoreboard players operation #st_d mgs.data %= #10 mgs.data
function mgs:v5.4.4/stats/menu/zb_dialog with storage mgs:temp _sv.d

