
#> mgs:v5.1.0/zombies/inventory/place_perk_at/tombstone
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/inventory/place_perk/tombstone with storage mgs:temp _perk_place
#
# @args		slot (unknown)
#

$item replace entity @s inventory.$(slot) with minecraft:paper[item_model="mgs:perk_machine_tombstone",custom_data={mgs:{zb_perk_display:true}},item_name={"translate":"mgs.tombstone","color":"gold","italic":false},lore=[{"translate":"mgs.if_you_bleed_out_leave_a_tombstone","color":"gray","italic":false},{"translate":"mgs.return_to_it_the_next_round_to_recover","color":"gray","italic":false},{"translate":"mgs.your_perks_and_full_inventory","color":"gray","italic":false},{"translate":"mgs.owned_perk","color":"dark_gray","italic":false}]]

