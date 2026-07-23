
#> mgs:v5.1.0/zombies/inventory/place_perk_at/quick_revive
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/inventory/place_perk/quick_revive with storage mgs:temp _perk_place
#
# @args		slot (unknown)
#

$item replace entity @s inventory.$(slot) with minecraft:paper[item_model="mgs:perk_machine_quick_revive",custom_data={mgs:{zb_perk_display:true}},item_name={"translate":"mgs.quick_revive","color":"aqua","italic":false},lore=[{"translate":"mgs.revive_downed_teammates_faster","color":"gray","italic":false},{"translate":"mgs.solo_revives_you_after_you_go_down","color":"gray","italic":false},{"translate":"mgs.owned_perk","color":"dark_gray","italic":false}]]

