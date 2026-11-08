
#> mgs:v5.4.1/zombies/restart_no_map
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/restart
#

tag @a[tag=mgs.zb_restart] remove mgs.zb_restart
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.no_map_selected_open_the_setup_menu_first","fallback":"No map selected. Open the setup menu first.","color":"red"}]

