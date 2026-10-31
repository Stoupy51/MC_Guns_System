
#> mgs:v5.3.0/stats/menu/mp_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/menu/mp with storage mgs:temp _sv.d
#
# @args		i (unknown)
#			name (unknown)
#			games (unknown)
#			wins (unknown)
#			losses (unknown)
#			kills (unknown)
#			deaths (unknown)
#			headshots (unknown)
#			captures (unknown)
#			plants (unknown)
#			defuses (unknown)
#			objectives (unknown)
#			time_h (unknown)
#			time_m (unknown)
#			kd_i (unknown)
#			kd_d (unknown)
#			win_rate_i (unknown)
#			win_rate_d (unknown)
#			ffa_wins (unknown)
#			ffa_games (unknown)
#			tdm_wins (unknown)
#			tdm_games (unknown)
#			dom_wins (unknown)
#			dom_games (unknown)
#			hp_wins (unknown)
#			hp_games (unknown)
#			snd_wins (unknown)
#			snd_games (unknown)
#			demo_wins (unknown)
#			demo_games (unknown)
#

$scoreboard players set #st_t mgs.data $(i)
scoreboard players operation #st_t mgs.data *= #4 mgs.data
scoreboard players add #st_t mgs.data 99999
execute store result storage mgs:temp _sv.t.trigger_zb int 1 run scoreboard players add #st_t mgs.data 1
execute store result storage mgs:temp _sv.t.trigger_mp int 1 run scoreboard players add #st_t mgs.data 1
execute store result storage mgs:temp _sv.t.trigger_mi int 1 run scoreboard players add #st_t mgs.data 1
$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["",{text:"$(name)",color:"gold",bold:true},[{text:" - ",color:"yellow"}, {translate:"mgs.multiplayer",fallback:"Multiplayer"}]],body:[{type:"minecraft:plain_message",width:300,contents:["",{translate:"mgs.games_played",fallback:"Games played",color:"gray"},": ",{text:"$(games)",color:"white"},"\n",{translate:"mgs.wins_3",fallback:"Wins",color:"gray"},": ",{text:"$(wins)",color:"white"},"\n",{translate:"mgs.losses",fallback:"Losses",color:"gray"},": ",{text:"$(losses)",color:"white"},"\n",{translate:"mgs.kills_3",fallback:"Kills",color:"gray"},": ",{text:"$(kills)",color:"white"},"\n",{translate:"mgs.deaths_2",fallback:"Deaths",color:"gray"},": ",{text:"$(deaths)",color:"white"},"\n",{translate:"mgs.headshots",fallback:"Headshots",color:"gray"},": ",{text:"$(headshots)",color:"white"},"\n",{translate:"mgs.captures",fallback:"Captures",color:"gray"},": ",{text:"$(captures)",color:"white"},"\n",{translate:"mgs.bomb_plants",fallback:"Bomb plants",color:"gray"},": ",{text:"$(plants)",color:"white"},"\n",{translate:"mgs.bomb_defuses",fallback:"Bomb defuses",color:"gray"},": ",{text:"$(defuses)",color:"white"},"\n",{translate:"mgs.objectives",fallback:"Objectives",color:"gray"},": ",{text:"$(objectives)",color:"white"},"\n",{translate:"mgs.time_played",fallback:"Time played",color:"gray"},": ",{text:"$(time_h)h $(time_m)m",color:"white"},"\n",{text:"K/D",color:"gray"},": ",{text:"$(kd_i).$(kd_d)",color:"white"},"\n",{translate:"mgs.win_rate",fallback:"Win rate",color:"gray"},": ",{text:"$(win_rate_i).$(win_rate_d)%",color:"white"},"\n",{translate:"mgs.free_for_all",fallback:"Free For All",color:"gray"},": ",{text:"$(ffa_wins) / $(ffa_games)",color:"white"},[{text:" ",color:"gray"}, {translate:"mgs.wins_2",fallback:"wins"}],"\n",{translate:"mgs.team_deathmatch",fallback:"Team Deathmatch",color:"gray"},": ",{text:"$(tdm_wins) / $(tdm_games)",color:"white"},[{text:" ",color:"gray"}, {translate:"mgs.wins_2",fallback:"wins"}],"\n",{translate:"mgs.domination",fallback:"Domination",color:"gray"},": ",{text:"$(dom_wins) / $(dom_games)",color:"white"},[{text:" ",color:"gray"}, {translate:"mgs.wins_2",fallback:"wins"}],"\n",{translate:"mgs.hardpoint",fallback:"Hardpoint",color:"gray"},": ",{text:"$(hp_wins) / $(hp_games)",color:"white"},[{text:" ",color:"gray"}, {translate:"mgs.wins_2",fallback:"wins"}],"\n",{translate:"mgs.search_and_destroy",fallback:"Search and Destroy",color:"gray"},": ",{text:"$(snd_wins) / $(snd_games)",color:"white"},[{text:" ",color:"gray"}, {translate:"mgs.wins_2",fallback:"wins"}],"\n",{translate:"mgs.demolition",fallback:"Demolition",color:"gray"},": ",{text:"$(demo_wins) / $(demo_games)",color:"white"},[{text:" ",color:"gray"}, {translate:"mgs.wins_2",fallback:"wins"}]]}],actions:[],columns:3,after_action:"close",exit_action:{label:{translate:"gui.done"}}}
function mgs:v5.3.0/stats/menu/mp_tabs with storage mgs:temp _sv.t
function mgs:v5.3.0/multiplayer/show_dialog with storage mgs:temp

