
#> mgs:v5.3.0/stats/menu/mi_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/menu/mi with storage mgs:temp _sv.d
#
# @args		i (unknown)
#			name (unknown)
#			games (unknown)
#			completed (unknown)
#			kills (unknown)
#			headshots (unknown)
#			deaths (unknown)
#			time_h (unknown)
#			time_m (unknown)
#			kd_i (unknown)
#			kd_d (unknown)
#

$scoreboard players set #st_t mgs.data $(i)
scoreboard players operation #st_t mgs.data *= #4 mgs.data
scoreboard players add #st_t mgs.data 99999
execute store result storage mgs:temp _sv.t.trigger_zb int 1 run scoreboard players add #st_t mgs.data 1
execute store result storage mgs:temp _sv.t.trigger_mp int 1 run scoreboard players add #st_t mgs.data 1
execute store result storage mgs:temp _sv.t.trigger_mi int 1 run scoreboard players add #st_t mgs.data 1
$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["",{text:"$(name)",color:"gold",bold:true},[{text:" - ",color:"yellow"}, {translate:"mgs.missions",fallback:"Missions"}]],body:[{type:"minecraft:plain_message",width:300,contents:["",{translate:"mgs.missions_played",fallback:"Missions played",color:"gray"},": ",{text:"$(games)",color:"white"},"\n",{translate:"mgs.completed",fallback:"Completed",color:"gray"},": ",{text:"$(completed)",color:"white"},"\n",{translate:"mgs.kills_3",fallback:"Kills",color:"gray"},": ",{text:"$(kills)",color:"white"},"\n",{translate:"mgs.headshots",fallback:"Headshots",color:"gray"},": ",{text:"$(headshots)",color:"white"},"\n",{translate:"mgs.deaths_2",fallback:"Deaths",color:"gray"},": ",{text:"$(deaths)",color:"white"},"\n",{translate:"mgs.time_played",fallback:"Time played",color:"gray"},": ",{text:"$(time_h)h $(time_m)m",color:"white"},"\n",{text:"K/D",color:"gray"},": ",{text:"$(kd_i).$(kd_d)",color:"white"}]}],actions:[],columns:3,after_action:"close",exit_action:{label:{translate:"gui.done"}}}
function mgs:v5.3.0/stats/menu/mi_tabs with storage mgs:temp _sv.t
function mgs:v5.3.0/multiplayer/show_dialog with storage mgs:temp

