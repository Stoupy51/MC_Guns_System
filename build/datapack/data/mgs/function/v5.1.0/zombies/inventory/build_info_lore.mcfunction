
#> mgs:v5.1.0/zombies/inventory/build_info_lore
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/inventory/refresh_info_item with storage mgs:temp info
#
# @args		round (unknown)
#			points (unknown)
#			kills (unknown)
#			downs (unknown)
#

$data modify storage mgs:temp info.lore set value [{"text":"Round: $(round)","color":"gray","italic":false},{"text":"Points: $(points)","color":"gray","italic":false},{"text":"Kills: $(kills)","color":"gray","italic":false},{"text":"Downs: $(downs)","color":"gray","italic":false}]

