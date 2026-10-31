
#> mgs:v5.3.0/stats/menu/players_list
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/menu/players_page {kind:"view",title:"Players"}
#			mgs:v5.3.0/stats/admin/players {kind:"reset",title:"Reset Player Stats"}
#
# @args		kind (string)
#			title (string)
#

scoreboard players operation #st_i mgs.data = #st_page mgs.data
scoreboard players operation #st_i mgs.data *= #10 mgs.data
scoreboard players operation #st_end mgs.data = #st_i mgs.data
scoreboard players add #st_end mgs.data 10
execute store result score #st_total mgs.data run data get storage mgs:stats known

data modify storage mgs:temp _sp set value {}
$data modify storage mgs:temp _sp.kind set value "$(kind)"
execute store result storage mgs:temp _sp.total int 1 run scoreboard players get #st_total mgs.data
$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","👥 ",{text:"$(title)",color:"gold",bold:true}],body:[],actions:[],columns:2,after_action:"close",exit_action:{label:{translate:"gui.done"}}}
function mgs:v5.3.0/stats/menu/players_body with storage mgs:temp _sp
function mgs:v5.3.0/stats/menu/players_next

execute store result storage mgs:temp _sp.page int 1 run scoreboard players remove #st_page mgs.data 1
execute store result storage mgs:temp _sp.page_trigger int 1 run scoreboard players add #st_page mgs.data 90000
$execute if score #st_page mgs.data matches 90000.. run function mgs:v5.3.0/stats/menu/players_prev_$(kind) with storage mgs:temp _sp
execute store result storage mgs:temp _sp.page int 1 run scoreboard players remove #st_page mgs.data 89998
execute store result storage mgs:temp _sp.page_trigger int 1 run scoreboard players add #st_page mgs.data 90000
$execute if score #st_end mgs.data < #st_total mgs.data run function mgs:v5.3.0/stats/menu/players_more_$(kind) with storage mgs:temp _sp
function mgs:v5.3.0/multiplayer/show_dialog with storage mgs:temp

