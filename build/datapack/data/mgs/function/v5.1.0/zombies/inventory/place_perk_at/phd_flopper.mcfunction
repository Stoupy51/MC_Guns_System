
#> mgs:v5.1.0/zombies/inventory/place_perk_at/phd_flopper
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/inventory/place_perk/phd_flopper with storage mgs:temp _perk_place
#
# @args		slot (unknown)
#

$item replace entity @s inventory.$(slot) with minecraft:paper[item_model="mgs:perk_machine_phd_flopper",custom_data={mgs:{zb_perk_display:true}},item_name={"translate":"mgs.phd_flopper","color":"dark_purple","italic":false},lore=[{"translate":"mgs.immune_to_fall_and_self_explosive_damage","color":"gray","italic":false},{"translate":"mgs.dive_to_prone_to_set_off_a_blast","color":"gray","italic":false},{"translate":"mgs.owned_perk","color":"dark_gray","italic":false}]]

