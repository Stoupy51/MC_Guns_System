
#> mgs:v5.3.0/stats/board/holo_show
#
# @executed	at @s
#
# @within	mgs:v5.3.0/stats/board/holo_one
#

tag @s add mgs.lb_shown
function mgs:v5.3.0/stats/board/render with entity @s data.lb
execute if data entity @s data.lb{kind:"level_mp"} run data modify storage mgs:temp _lb_text set value ["",{translate:"mgs.multiplayer_level_2",fallback:"Multiplayer Level",color:"gold",bold:true},"\n"]
execute if data entity @s data.lb{kind:"level_zb"} run data modify storage mgs:temp _lb_text set value ["",{translate:"mgs.zombies_level_2",fallback:"Zombies Level",color:"gold",bold:true},"\n"]
execute if data entity @s data.lb{kind:"zb_map"} run data modify storage mgs:temp _lb_text set value ["",{translate:"mgs.best_rounds",fallback:"Best Rounds",color:"gold",bold:true},"\n"]
execute if data entity @s data.lb{kind:"mi_map"} run data modify storage mgs:temp _lb_text set value ["",{translate:"mgs.best_times",fallback:"Best Times",color:"gold",bold:true},"\n"]
data modify storage mgs:temp _lb_text append from storage mgs:temp _lb_lines[]
execute unless data storage mgs:temp _lb_lines[0] run data modify storage mgs:temp _lb_text append value {translate:"mgs.no_entries_yet",fallback:"No entries yet",color:"gray"}
summon minecraft:text_display ~ ~ ~ {Tags:["mgs.lb_text","mgs.zombies_entity","mgs.lb_new"],billboard:"vertical",alignment:"center",default_background:true}
data modify entity @n[type=minecraft:text_display,tag=mgs.lb_new] text set from storage mgs:temp _lb_text
tag @e[type=minecraft:text_display,tag=mgs.lb_new] remove mgs.lb_new

