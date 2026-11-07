
#> mgs:v5.4.0/stats/board/dispatch
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/player/config/process
#

execute if score @s mgs.player.config matches 1630 run return run function mgs:v5.4.0/stats/board/menu
execute if score @s mgs.player.config matches 1631 run return run function mgs:v5.4.0/stats/board/show {path:"level_mp",kind:"level_mp",title:"Multiplayer Level",filters:0b}
execute if score @s mgs.player.config matches 1632 run return run function mgs:v5.4.0/stats/board/show {path:"level_zb",kind:"level_zb",title:"Zombies Level",filters:0b}
execute if score @s mgs.player.config matches 1633 run return run function mgs:v5.4.0/stats/board/maps {mode:"zombies",base:3000,step:8}
execute if score @s mgs.player.config matches 1634 run return run function mgs:v5.4.0/stats/board/maps {mode:"missions",base:2000,step:1}
execute if score @s mgs.player.config matches 3000..3999 run return run function mgs:v5.4.0/stats/board/zb_map_trigger
execute if score @s mgs.player.config matches 2000..2999 run return run function mgs:v5.4.0/stats/board/mi_map_trigger

