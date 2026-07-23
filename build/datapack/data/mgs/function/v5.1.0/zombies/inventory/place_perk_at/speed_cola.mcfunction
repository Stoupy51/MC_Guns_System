
#> mgs:v5.1.0/zombies/inventory/place_perk_at/speed_cola
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/inventory/place_perk/speed_cola with storage mgs:temp _perk_place
#
# @args		slot (unknown)
#

$item replace entity @s inventory.$(slot) with minecraft:paper[item_model="mgs:perk_machine_speed_cola",custom_data={mgs:{zb_perk_display:true}},item_name={"translate":"mgs.speed_cola","color":"green","italic":false},lore=[{"translate":"mgs.reload_all_your_weapons_much_faster","color":"gray","italic":false},{"translate":"mgs.about_twice_the_reload_speed","color":"gray","italic":false},{"translate":"mgs.owned_perk","color":"dark_gray","italic":false}]]

