
#> mgs:v5.4.2/zombies/save/rebuild_weapons
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/restore_player
#

summon minecraft:item_display ~ ~ ~ {Tags:["mgs.sv_rebuild","mgs.zombies_entity"]}
data modify storage mgs:temp _sv_items set value []
data modify storage mgs:temp _sv_source set from storage mgs:temp _sv_player.inventory
execute if data storage mgs:temp _sv_source[0] run function mgs:v5.4.2/zombies/save/rebuild_next
kill @e[type=minecraft:item_display,tag=mgs.sv_rebuild]
data remove storage mgs:temp _sv_source

