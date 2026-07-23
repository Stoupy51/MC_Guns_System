
#> mgs:v5.1.0/zombies/inventory/place_perk_at/double_tap
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/inventory/place_perk/double_tap with storage mgs:temp _perk_place
#
# @args		slot (unknown)
#

$item replace entity @s inventory.$(slot) with minecraft:paper[item_model="mgs:perk_machine_double_tap",custom_data={mgs:{zb_perk_display:true}},item_name={"translate":"mgs.double_tap","color":"yellow","italic":false},lore=[{"translate":"mgs.fires_an_extra_bullet_with_every_shot","color":"gray","italic":false},{"translate":"mgs.roughly_doubles_your_damage_output","color":"gray","italic":false},{"translate":"mgs.owned_perk","color":"dark_gray","italic":false}]]

