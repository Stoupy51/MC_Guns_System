
#> mgs:v5.1.0/zombies/inventory/place_perk_at/stamin_up
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/inventory/place_perk/stamin_up with storage mgs:temp _perk_place
#
# @args		slot (unknown)
#

$item replace entity @s inventory.$(slot) with minecraft:paper[item_model="mgs:perk_machine_stamin_up",custom_data={mgs:{zb_perk_display:true}},item_name={"translate":"mgs.stamin_up","color":"gold","italic":false},lore=[{"translate":"mgs.move_faster_and_sprint_for_longer","color":"gray","italic":false},[{"text":"+7% ","color":"gray","italic":false}, {"translate":"mgs.move_speed_double_sprint_endurance"}],{"translate":"mgs.owned_perk","color":"dark_gray","italic":false}]]

