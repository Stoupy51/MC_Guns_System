
#> mgs:v5.0.1/zombies/inventory/refresh_info_item_render
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.0.1/zombies/inventory/refresh_info_item with storage mgs:temp info
#
# @args		lore (unknown)
#

$item replace entity @s hotbar.8 with minecraft:paper[custom_data={mgs:{zb_info:true}},item_name={"text":"\u2139 Player Info","color":"gold","italic":false},lore=$(lore)]

