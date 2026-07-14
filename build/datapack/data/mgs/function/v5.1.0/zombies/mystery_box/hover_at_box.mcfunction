
#> mgs:v5.1.0/zombies/mystery_box/hover_at_box
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/mystery_box/on_hover [ at @n[tag=bs.interaction.target] ]
#

execute if entity @n[tag=mgs.mb_display,distance=..3,scores={mgs.mb.anim=1..}] run return run function mgs:v5.1.0/zombies/mystery_box/hud_spinning
execute if entity @n[tag=mgs.mb_display,distance=..3] run return run function mgs:v5.1.0/zombies/mystery_box/hud_ready
function mgs:v5.1.0/zombies/mystery_box/hud_price

