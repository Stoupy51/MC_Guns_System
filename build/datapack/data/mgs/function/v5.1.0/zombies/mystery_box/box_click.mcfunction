
#> mgs:v5.1.0/zombies/mystery_box/box_click
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/mystery_box/on_right_click [ at @n[tag=bs.interaction.target] ]
#

# Spinning (a pull display here with anim > 0): already in use
execute if entity @n[tag=mgs.mb_display,distance=..3,scores={mgs.mb.anim=1..}] run return run function mgs:v5.1.0/zombies/mystery_box/deny_already_in_use

# Ready (a display here, anim <= 0): only the buyer of this box may collect (buyer pid matches)
execute if entity @n[tag=mgs.mb_display,distance=..3] if score @s mgs.mb.pid = @n[tag=mgs.mb_display,distance=..3] mgs.mb.buyer run return run function mgs:v5.1.0/zombies/mystery_box/collect
execute if entity @n[tag=mgs.mb_display,distance=..3] run return run function mgs:v5.1.0/zombies/mystery_box/deny_not_your_result

# No pull on this box yet: start one
function mgs:v5.1.0/zombies/mystery_box/try_use

