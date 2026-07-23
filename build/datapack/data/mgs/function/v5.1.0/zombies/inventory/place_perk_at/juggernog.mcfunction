
#> mgs:v5.1.0/zombies/inventory/place_perk_at/juggernog
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/inventory/place_perk/juggernog with storage mgs:temp _perk_place
#
# @args		slot (unknown)
#

$item replace entity @s inventory.$(slot) with minecraft:paper[item_model="mgs:perk_machine_juggernog",custom_data={mgs:{zb_perk_display:true}},item_name={"translate":"mgs.juggernog","color":"red","italic":false},lore=[{"translate":"mgs.raises_your_max_health_to_40_x4","color":"gray","italic":false},{"translate":"mgs.survive_far_more_hits_before_going_down","color":"gray","italic":false},{"translate":"mgs.owned_perk","color":"dark_gray","italic":false}]]

