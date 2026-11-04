
#> mgs:v5.3.0/zombies/inventory/build_info_lore
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zombies/inventory/refresh_info_item with storage mgs:temp info
#
# @args		round (unknown)
#			points (unknown)
#			kills (unknown)
#			downs (unknown)
#

$data modify storage mgs:temp info.lore set value [{"text":"Round: $(round)","color":"gray","italic":false},{"text":"Points: $(points)","color":"gray","italic":false},{"text":"Kills: $(kills)","color":"gray","italic":false},{"text":"Downs: $(downs)","color":"gray","italic":false}]

