
#> mgs:v5.1.0/zombies/inventory/place_perk_at/whos_who
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/inventory/place_perk/whos_who with storage mgs:temp _perk_place
#
# @args		slot (unknown)
#

$item replace entity @s inventory.$(slot) with minecraft:paper[item_model="mgs:perk_machine_whos_who",custom_data={mgs:{zb_perk_display:true}},item_name={"translate":"mgs.whos_who","color":"dark_aqua","italic":false},lore=[{"translate":"mgs.when_downed_fight_on_as_a_clone","color":"gray","italic":false},{"translate":"mgs.revive_your_own_body_to_fully_recover","color":"gray","italic":false},{"translate":"mgs.co_op_only","color":"gray","italic":false},{"translate":"mgs.owned_perk","color":"dark_gray","italic":false}]]

