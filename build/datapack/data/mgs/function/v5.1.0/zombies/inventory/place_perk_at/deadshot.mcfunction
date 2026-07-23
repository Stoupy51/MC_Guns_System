
#> mgs:v5.1.0/zombies/inventory/place_perk_at/deadshot
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/inventory/place_perk/deadshot with storage mgs:temp _perk_place
#
# @args		slot (unknown)
#

$item replace entity @s inventory.$(slot) with minecraft:paper[item_model="mgs:perk_machine_deadshot",custom_data={mgs:{zb_perk_display:true}},item_name={"translate":"mgs.deadshot_daiquiri","color":"dark_green","italic":false},lore=[{"translate":"mgs.aim_snaps_toward_zombie_heads","color":"gray","italic":false},{"translate":"mgs.tighter_hipfire_spread_and_less_recoil","color":"gray","italic":false},{"translate":"mgs.owned_perk","color":"dark_gray","italic":false}]]

