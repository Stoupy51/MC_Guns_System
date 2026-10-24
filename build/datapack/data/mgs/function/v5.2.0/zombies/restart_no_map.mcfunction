
#> mgs:v5.2.0/zombies/restart_no_map
#
# @executed	as the player & at current position
#
# @within	mgs:v5.2.0/zombies/restart
#

tag @a[tag=mgs.zb_restart] remove mgs.zb_restart
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.no_map_selected_open_the_setup_menu_first","fallback":"No map selected. Open the setup menu first.","color":"red"}]

