
#> mgs:v5.1.0/zombies/wunderfizz/machine_click
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/wunderfizz/on_right_click [ at @n[tag=bs.interaction.target] ]
#

# Spinning here → in use
execute if entity @n[type=item_display,tag=mgs.wunderfizz_orb,distance=..3,scores={mgs.zb.wf.anim=1..}] run return run function mgs:v5.1.0/zombies/wunderfizz/deny_in_use

# A ready orb here → only the buyer may collect
execute if entity @n[type=item_display,tag=mgs.wunderfizz_orb,distance=..3] if score @s mgs.zb.wf_pid = @n[type=item_display,tag=mgs.wunderfizz_orb,distance=..3] mgs.zb.wf.buyer run return run function mgs:v5.1.0/zombies/wunderfizz/collect
execute if entity @n[type=item_display,tag=mgs.wunderfizz_orb,distance=..3] run return run function mgs:v5.1.0/zombies/wunderfizz/deny_not_your_result

# Nothing here yet: start a spin
function mgs:v5.1.0/zombies/wunderfizz/try_use

