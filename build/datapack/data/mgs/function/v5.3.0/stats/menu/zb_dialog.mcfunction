
#> mgs:v5.3.0/stats/menu/zb_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/menu/zb with storage mgs:temp _sv.d
#
# @args		i (unknown)
#			name (unknown)
#			games (unknown)
#			rounds (unknown)
#			best_round (unknown)
#			kills (unknown)
#			headshots (unknown)
#			downs (unknown)
#			deaths (unknown)
#			revives (unknown)
#			points_earned (unknown)
#			points_spent (unknown)
#			doors (unknown)
#			boxes (unknown)
#			wallbuys (unknown)
#			perks (unknown)
#			pap (unknown)
#			traps (unknown)
#			powerups (unknown)
#			barricades (unknown)
#			power (unknown)
#			time_h (unknown)
#			time_m (unknown)
#

$scoreboard players set #st_t mgs.data $(i)
scoreboard players operation #st_t mgs.data *= #4 mgs.data
scoreboard players add #st_t mgs.data 99999
execute store result storage mgs:temp _sv.t.trigger_zb int 1 run scoreboard players add #st_t mgs.data 1
execute store result storage mgs:temp _sv.t.trigger_mp int 1 run scoreboard players add #st_t mgs.data 1
execute store result storage mgs:temp _sv.t.trigger_mi int 1 run scoreboard players add #st_t mgs.data 1
$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["",{text:"$(name)",color:"gold",bold:true},[{text:" - ",color:"yellow"}, {translate:"mgs.zombies",fallback:"Zombies"}]],body:[{type:"minecraft:plain_message",width:300,contents:["",{translate:"mgs.games_played",fallback:"Games played",color:"gray"},": ",{text:"$(games)",color:"white"},"\n",{translate:"mgs.rounds_survived",fallback:"Rounds survived",color:"gray"},": ",{text:"$(rounds)",color:"white"},"\n",{translate:"mgs.best_round",fallback:"Best round",color:"gray"},": ",{text:"$(best_round)",color:"white"},"\n",{translate:"mgs.kills_3",fallback:"Kills",color:"gray"},": ",{text:"$(kills)",color:"white"},"\n",{translate:"mgs.headshots",fallback:"Headshots",color:"gray"},": ",{text:"$(headshots)",color:"white"},"\n",{translate:"mgs.downs",fallback:"Downs",color:"gray"},": ",{text:"$(downs)",color:"white"},"\n",{translate:"mgs.bleed_outs",fallback:"Bleed-outs",color:"gray"},": ",{text:"$(deaths)",color:"white"},"\n",{translate:"mgs.revives",fallback:"Revives",color:"gray"},": ",{text:"$(revives)",color:"white"},"\n",{translate:"mgs.points_earned",fallback:"Points earned",color:"gray"},": ",{text:"$(points_earned)",color:"white"},"\n",{translate:"mgs.points_spent",fallback:"Points spent",color:"gray"},": ",{text:"$(points_spent)",color:"white"},"\n",{translate:"mgs.doors_opened",fallback:"Doors opened",color:"gray"},": ",{text:"$(doors)",color:"white"},"\n",{translate:"mgs.mystery_boxes",fallback:"Mystery boxes",color:"gray"},": ",{text:"$(boxes)",color:"white"},"\n",{translate:"mgs.wall_weapons_bought",fallback:"Wall weapons bought",color:"gray"},": ",{text:"$(wallbuys)",color:"white"},"\n",{translate:"mgs.perks",fallback:"Perks",color:"gray"},": ",{text:"$(perks)",color:"white"},"\n",{translate:"mgs.pack_a_punch_2",fallback:"Pack-a-Punch",color:"gray"},": ",{text:"$(pap)",color:"white"},"\n",{translate:"mgs.traps",fallback:"Traps",color:"gray"},": ",{text:"$(traps)",color:"white"},"\n",{translate:"mgs.power_ups",fallback:"Power-ups",color:"gray"},": ",{text:"$(powerups)",color:"white"},"\n",{translate:"mgs.barricades_repaired",fallback:"Barricades repaired",color:"gray"},": ",{text:"$(barricades)",color:"white"},"\n",{translate:"mgs.power_turned_on",fallback:"Power turned on",color:"gray"},": ",{text:"$(power)",color:"white"},"\n",{translate:"mgs.time_played",fallback:"Time played",color:"gray"},": ",{text:"$(time_h)h $(time_m)m",color:"white"}]}],actions:[],columns:3,after_action:"close",exit_action:{label:{translate:"gui.done"}}}
function mgs:v5.3.0/stats/menu/zb_tabs with storage mgs:temp _sv.t
function mgs:v5.3.0/multiplayer/show_dialog with storage mgs:temp

