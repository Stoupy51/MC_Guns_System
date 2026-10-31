
#> mgs:v5.3.0/stats/menu/mp
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/menu/view
#

data modify storage mgs:temp _sv.d set from storage mgs:temp _sv.p.mp
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
execute store result score #st_n mgs.data run data get storage mgs:temp _sv.d.wins 1000
execute store result score #st_d mgs.data run data get storage mgs:temp _sv.d.games
execute if score #st_d mgs.data matches 0 run scoreboard players set #st_d mgs.data 1
scoreboard players operation #st_n mgs.data /= #st_d mgs.data
scoreboard players operation #st_d mgs.data = #st_n mgs.data
execute store result storage mgs:temp _sv.d.win_rate_i int 1 run scoreboard players operation #st_n mgs.data /= #10 mgs.data
execute store result storage mgs:temp _sv.d.win_rate_d int 1 run scoreboard players operation #st_d mgs.data %= #10 mgs.data
data modify storage mgs:temp _sv.d.ffa_games set from storage mgs:temp _sv.p.mp.modes.ffa.games
data modify storage mgs:temp _sv.d.ffa_wins set from storage mgs:temp _sv.p.mp.modes.ffa.wins
data modify storage mgs:temp _sv.d.tdm_games set from storage mgs:temp _sv.p.mp.modes.tdm.games
data modify storage mgs:temp _sv.d.tdm_wins set from storage mgs:temp _sv.p.mp.modes.tdm.wins
data modify storage mgs:temp _sv.d.dom_games set from storage mgs:temp _sv.p.mp.modes.dom.games
data modify storage mgs:temp _sv.d.dom_wins set from storage mgs:temp _sv.p.mp.modes.dom.wins
data modify storage mgs:temp _sv.d.hp_games set from storage mgs:temp _sv.p.mp.modes.hp.games
data modify storage mgs:temp _sv.d.hp_wins set from storage mgs:temp _sv.p.mp.modes.hp.wins
data modify storage mgs:temp _sv.d.snd_games set from storage mgs:temp _sv.p.mp.modes.snd.games
data modify storage mgs:temp _sv.d.snd_wins set from storage mgs:temp _sv.p.mp.modes.snd.wins
data modify storage mgs:temp _sv.d.demo_games set from storage mgs:temp _sv.p.mp.modes.demo.games
data modify storage mgs:temp _sv.d.demo_wins set from storage mgs:temp _sv.p.mp.modes.demo.wins
function mgs:v5.3.0/stats/menu/mp_dialog with storage mgs:temp _sv.d

