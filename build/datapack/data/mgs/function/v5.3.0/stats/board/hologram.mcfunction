
#> mgs:v5.3.0/stats/board/hologram
#
# @executed	positioned ~ ~0.5 ~
#
# @within	mgs:leaderboard/level_mp [ positioned ~ ~0.5 ~ ]
#			mgs:leaderboard/level_zb [ positioned ~ ~0.5 ~ ]
#			mgs:leaderboard/zb_map [ positioned ~ ~0.5 ~ ]
#			mgs:leaderboard/mi_map [ positioned ~ ~0.5 ~ ]
#

execute unless entity @a[distance=..24] run return run kill @e[type=minecraft:text_display,tag=mgs.lb_text,distance=..0.1]
execute if entity @e[type=minecraft:text_display,tag=mgs.lb_text,distance=..0.1] run return 0

function mgs:v5.3.0/stats/board/render with storage mgs:temp _lb_cb
data modify storage mgs:temp _lb_text set value ["",{text:"",color:"gold",bold:true},"\n"]
data modify storage mgs:temp _lb_text[1].text set from storage mgs:temp _lb_cb.title
data modify storage mgs:temp _lb_text append from storage mgs:temp _lb_lines[]
execute unless data storage mgs:temp _lb_lines[0] run data modify storage mgs:temp _lb_text append value {translate:"mgs.no_entries_yet",fallback:"No entries yet",color:"gray"}
summon minecraft:text_display ~ ~ ~ {Tags:["mgs.lb_text","mgs.lb_new"],billboard:"vertical",alignment:"center",default_background:true}
data modify entity @n[type=minecraft:text_display,tag=mgs.lb_new] text set from storage mgs:temp _lb_text
tag @e[type=minecraft:text_display,tag=mgs.lb_new] remove mgs.lb_new

