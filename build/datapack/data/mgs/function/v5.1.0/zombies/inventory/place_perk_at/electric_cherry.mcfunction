
#> mgs:v5.1.0/zombies/inventory/place_perk_at/electric_cherry
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/inventory/place_perk/electric_cherry with storage mgs:temp _perk_place
#
# @args		slot (unknown)
#

$item replace entity @s inventory.$(slot) with minecraft:paper[item_model="mgs:perk_machine_electric_cherry",custom_data={mgs:{zb_perk_display:true}},item_name={"translate":"mgs.electric_cherry","color":"blue","italic":false},lore=[{"translate":"mgs.reloading_discharges_a_shockwave","color":"gray","italic":false},{"translate":"mgs.damages_and_stuns_nearby_zombies","color":"gray","italic":false},{"translate":"mgs.stronger_the_emptier_your_magazine","color":"gray","italic":false},{"translate":"mgs.owned_perk","color":"dark_gray","italic":false}]]

