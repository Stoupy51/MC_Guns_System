
#> mgs:v5.1.0/zombies/inventory/place_perk_at/timeslip
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/inventory/place_perk/timeslip with storage mgs:temp _perk_place
#
# @args		slot (unknown)
#

$item replace entity @s inventory.$(slot) with minecraft:paper[item_model="mgs:perk_machine_timeslip",custom_data={mgs:{zb_perk_display:true}},item_name={"translate":"mgs.timeslip","color":"light_purple","italic":false},lore=[{"translate":"mgs.machines_and_power_ups_spin_faster","color":"gray","italic":false},{"translate":"mgs.pack_a_punch_box_wunderfizz_speed_up","color":"gray","italic":false},{"translate":"mgs.grenades_throw_on_a_shorter_cooldown","color":"gray","italic":false},{"translate":"mgs.owned_perk","color":"dark_gray","italic":false}]]

