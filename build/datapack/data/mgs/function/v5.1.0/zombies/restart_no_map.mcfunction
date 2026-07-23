
#> mgs:v5.1.0/zombies/restart_no_map
#
# @within	mgs:v5.1.0/zombies/restart
#

tag @a[tag=mgs.zb_restart] remove mgs.zb_restart
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_map_selected_open_the_setup_menu_first","color":"red"}]

