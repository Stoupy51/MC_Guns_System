
#> mgs:v5.1.0/zombies/inventory/place_perk_at/mule_kick
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/inventory/place_perk/mule_kick with storage mgs:temp _perk_place
#
# @args		slot (unknown)
#

$item replace entity @s inventory.$(slot) with minecraft:paper[item_model="mgs:perk_machine_mule_kick",custom_data={mgs:{zb_perk_display:true}},item_name={"translate":"mgs.mule_kick","color":"dark_green","italic":false},lore=[{"translate":"mgs.carry_a_third_weapon","color":"gray","italic":false},{"translate":"mgs.unlocks_an_extra_weapon_slot","color":"gray","italic":false},{"translate":"mgs.owned_perk","color":"dark_gray","italic":false}]]

