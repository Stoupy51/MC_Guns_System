
#> mgs:v5.0.1/zombies/inventory/place_perk_item_at
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.0.1/zombies/inventory/place_perk_item with storage mgs:temp _perk_place
#
# @args		id (string)
#			name (string)
#			color (string)
#			slot (unknown)
#

$item replace entity @s inventory.$(slot) with minecraft:paper[item_model="mgs:perk_machine_$(id)",custom_data={mgs:{zb_perk_display:true}},item_name={"text":"$(name)","color":"$(color)","italic":false},lore=[{"translate":"mgs.owned_perk","color":"gray","italic":false}]]

