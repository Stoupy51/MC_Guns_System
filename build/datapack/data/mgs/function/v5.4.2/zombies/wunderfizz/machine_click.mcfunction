
#> mgs:v5.4.2/zombies/wunderfizz/machine_click
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/wunderfizz/on_right_click [ at @n[tag=bs.interaction.target] ]
#

execute if entity @n[type=item_display,tag=mgs.wunderfizz_orb,distance=..3,scores={mgs.zb.wf.anim=1..}] run return run function mgs:v5.4.2/zombies/deny/message {msg:'{"translate":"mgs.der_wunderfizz_is_already_spinning","fallback":"Der Wunderfizz is already spinning.","color":"red"}'}

# Only the buyer may collect.
execute if entity @n[type=item_display,tag=mgs.wunderfizz_orb,distance=..3] if score @s mgs.zb.wf_pid = @n[type=item_display,tag=mgs.wunderfizz_orb,distance=..3] mgs.zb.wf.buyer run return run function mgs:v5.4.2/zombies/wunderfizz/collect
execute if entity @n[type=item_display,tag=mgs.wunderfizz_orb,distance=..3] run return run function mgs:v5.4.2/zombies/deny/message {msg:'{"translate":"mgs.wait_for_the_buyer_to_collect_their_perk","fallback":"Wait for the buyer to collect their perk.","color":"red"}'}

function mgs:v5.4.2/zombies/wunderfizz/try_use

