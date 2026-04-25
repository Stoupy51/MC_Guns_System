
#> mgs:v5.0.0/zombies/inventory/refresh_info_item_render
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.0.0/zombies/inventory/refresh_info_item with storage mgs:temp info
#
# @args		round (unknown)
#			points (unknown)
#			kills (unknown)
#			downs (unknown)
#

$item replace entity @s hotbar.8 with minecraft:paper[custom_data={mgs:{zb_info:true}},item_name={"text":"\u2139 Player Info","color":"gold","italic":false},lore=[{"text":"Round: $(round)","color":"gray","italic":false},{"text":"Points: $(points)","color":"gray","italic":false},{"text":"Kills: $(kills)","color":"gray","italic":false},{"text":"Downs: $(downs)","color":"gray","italic":false}]]

