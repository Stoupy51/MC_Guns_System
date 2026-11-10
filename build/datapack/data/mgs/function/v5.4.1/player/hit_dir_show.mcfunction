
#> mgs:v5.4.1/player/hit_dir_show
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/weapon/hit_direction
#

# @s = the victim, #hit_dir = the sector to show. The other slot makes the new id differ from the applied one.
function mgs:v5.4.1/player/hit_dir_clear
execute store success score @s mgs.hit_dir_slot if score @s mgs.hit_dir_slot matches 0
scoreboard players operation @s mgs.hit_dir_sector = #hit_dir mgs.data

data modify storage mgs:input hit_dir set value {"sector":0,"slot":0}
execute store result storage mgs:input hit_dir.sector int 1 run scoreboard players get @s mgs.hit_dir_sector
execute store result storage mgs:input hit_dir.slot int 1 run scoreboard players get @s mgs.hit_dir_slot
function mgs:v5.4.1/player/hit_dir_add with storage mgs:input hit_dir

scoreboard players set @s mgs.hit_dir_off 15
scoreboard players operation @s mgs.hit_dir_off += #total_tick mgs.data

