
#> mgs:v5.1.0/zombies/inventory/place_perk_at/widows_wine
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/inventory/place_perk/widows_wine with storage mgs:temp _perk_place
#
# @args		slot (unknown)
#

$item replace entity @s inventory.$(slot) with minecraft:paper[item_model="mgs:perk_machine_widows_wine",custom_data={mgs:{zb_perk_display:true}},item_name={"translate":"mgs.widows_wine","color":"dark_red","italic":false},lore=[{"translate":"mgs.grenades_become_sticky_web_grenades","color":"gray","italic":false},{"translate":"mgs.being_hit_bursts_webbing_around_you","color":"gray","italic":false},{"translate":"mgs.stronger_melee_knife","color":"gray","italic":false},{"translate":"mgs.owned_perk","color":"dark_gray","italic":false}]]

