
#> mgs:v5.1.0/zombies/inventory/place_perk_at/dying_wish
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/inventory/place_perk/dying_wish with storage mgs:temp _perk_place
#
# @args		slot (unknown)
#

$item replace entity @s inventory.$(slot) with minecraft:paper[item_model="mgs:perk_machine_dying_wish",custom_data={mgs:{zb_perk_display:true}},item_name={"translate":"mgs.dying_wish","color":"blue","italic":false},lore=[{"translate":"mgs.cheat_death_when_you_would_go_down","color":"gray","italic":false},[{"translate":"mgs.brief_berserk_resistance_strength","color":"gray","italic":false}, ","],{"translate":"mgs.then_drop_to_1_hp_long_cooldown","color":"gray","italic":false},{"translate":"mgs.owned_perk","color":"dark_gray","italic":false}]]

