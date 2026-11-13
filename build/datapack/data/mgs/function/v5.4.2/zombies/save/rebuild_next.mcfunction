
#> mgs:v5.4.2/zombies/save/rebuild_next
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/rebuild_weapons
#			mgs:v5.4.2/zombies/save/rebuild_next
#

data modify storage mgs:temp _sv_item set from storage mgs:temp _sv_source[0]
execute if data storage mgs:temp _sv_item.components."minecraft:custom_data".mgs.gun run function mgs:v5.4.2/zombies/save/rebuild_gun with storage mgs:temp _sv_item.components."minecraft:custom_data".mgs.stats
data modify storage mgs:temp _sv_items append from storage mgs:temp _sv_item

data remove storage mgs:temp _sv_source[0]
execute if data storage mgs:temp _sv_source[0] run function mgs:v5.4.2/zombies/save/rebuild_next

