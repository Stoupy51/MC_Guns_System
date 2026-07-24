
#> mgs:v5.1.0/zombies/deny/message
#
# @executed	at @s
#
# @within	mgs:v5.1.0/maps/zombies/kino_der_toten/teleporter/on_theater_click {msg:'{"translate":"mgs.the_teleporter_is_recharging","color":"yellow"}'} [ at @s ]
#			mgs:v5.1.0/zombies/mystery_box/on_right_click {msg:'{"translate":"mgs.the_mystery_box_is_moving","color":"yellow"}'}
#			mgs:v5.1.0/zombies/mystery_box/share_at_box {msg:'{"translate":"mgs.wait_for_the_current_player_to_collect_their_result","color":"red"}'}
#			mgs:v5.1.0/zombies/mystery_box/box_click {msg:'{"translate":"mgs.mystery_box_is_already_in_use","color":"red"}'}
#			mgs:v5.1.0/zombies/mystery_box/box_click {msg:'{"translate":"mgs.wait_for_the_current_player_to_collect_their_result","color":"red"}'}
#			mgs:v5.1.0/zombies/mystery_box/result_all_owned {msg:'{"translate":"mgs.you_already_own_all_available_mystery_box_weapons_points_refunde","color":"yellow"}'} [ as @a[scores={mgs.zb.in_game=1}] ]
#			mgs:v5.1.0/zombies/pap/on_right_click {msg:'{"translate":"mgs.already_processing_a_weapon","color":"yellow"}'}
#			mgs:v5.1.0/zombies/pap/on_right_click {msg:'{"translate":"mgs.this_pack_a_punch_machine_requires_power","color":"red"}'}
#			mgs:v5.1.0/zombies/pap/on_right_click {msg:'{"translate":"mgs.hold_weapon_slot_1_2_or_3_to_use_pack_a_punch","color":"red"}'}
#			mgs:v5.1.0/zombies/pap/on_right_click {msg:'{"translate":"mgs.selected_slot_does_not_contain_a_weapon","color":"red"}'}
#			mgs:v5.1.0/zombies/pap/on_right_click {msg:'{"translate":"mgs.this_weapon_cannot_be_pack_a_punched","color":"red"}'}
#			mgs:v5.1.0/zombies/pap/anim/collect {msg:'{"translate":"mgs.this_upgraded_weapon_belongs_to_another_player","color":"red"}'}
#			mgs:v5.1.0/zombies/pap/upgrade_core {msg:'{"translate":"mgs.hold_weapon_slot_1_2_or_3_to_use_pack_a_punch","color":"red"}'}
#			mgs:v5.1.0/zombies/pap/upgrade_core {msg:'{"translate":"mgs.selected_slot_does_not_contain_a_weapon","color":"red"}'}
#			mgs:v5.1.0/zombies/pap/upgrade_core {msg:'{"translate":"mgs.this_weapon_cannot_be_pack_a_punched","color":"red"}'}
#			mgs:v5.1.0/zombies/power/on_activate {msg:'{"translate":"mgs.power_is_already_on","color":"yellow"}'}
#			mgs:v5.1.0/zombies/wallbuys/buy_knife {msg:'{"translate":"mgs.you_already_own_this_knife","color":"yellow"}'}
#			mgs:v5.1.0/zombies/wallbuys/refill_lethal {msg:'{"translate":"mgs.your_equipment_is_already_full","color":"yellow"}'}
#			mgs:v5.1.0/zombies/wallbuys/refill_tactical {msg:'{"translate":"mgs.your_equipment_is_already_full","color":"yellow"}'}
#			mgs:v5.1.0/zombies/perks/on_right_click {msg:'{"translate":"mgs.this_perk_machine_requires_power","color":"red"}'}
#			mgs:v5.1.0/zombies/perks/on_right_click {msg:'{"translate":"mgs.you_already_own_this_perk","color":"yellow"}'}
#			mgs:v5.1.0/zombies/wunderfizz/on_right_click {msg:'{"translate":"mgs.der_wunderfizz_is_moving_2","color":"yellow"}'}
#			mgs:v5.1.0/zombies/wunderfizz/on_right_click {msg:'{"translate":"mgs.this_der_wunderfizz_requires_power","color":"red"}'}
#			mgs:v5.1.0/zombies/wunderfizz/machine_click {msg:'{"translate":"mgs.der_wunderfizz_is_already_spinning","color":"red"}'}
#			mgs:v5.1.0/zombies/wunderfizz/machine_click {msg:'{"translate":"mgs.wait_for_the_buyer_to_collect_their_perk","color":"red"}'}
#			mgs:v5.1.0/zombies/wunderfizz/try_use {msg:'{"translate":"mgs.you_already_own_every_available_perk_points_refunded","color":"yellow"}'}
#			mgs:v5.1.0/zombies/traps/on_right_click {msg:'{"translate":"mgs.this_trap_requires_power","color":"red"}'}
#			mgs:v5.1.0/zombies/traps/on_right_click {msg:'{"translate":"mgs.trap_is_on_cooldown_and_not_ready_yet","color":"yellow"}'}
#
# @args		msg (string)
#

$tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],$(msg)]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

