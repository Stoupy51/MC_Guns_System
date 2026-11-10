
#> mgs:v5.4.1/player/hit_dir_clear
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/player/hit_dir_show
#			mgs:v5.4.1/player/hit_dir_expire
#

# @s = a player, possibly with an arc applied
execute unless score @s mgs.hit_dir_sector matches -2147483648.. run return 0
data modify storage mgs:input hit_dir set value {"sector":0,"slot":0}
execute store result storage mgs:input hit_dir.sector int 1 run scoreboard players get @s mgs.hit_dir_sector
execute store result storage mgs:input hit_dir.slot int 1 run scoreboard players get @s mgs.hit_dir_slot
function mgs:v5.4.1/player/hit_dir_remove with storage mgs:input hit_dir
scoreboard players reset @s mgs.hit_dir_sector

