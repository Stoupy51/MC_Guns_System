
#> mgs:v5.1.0/zombies/mystery_box/hover_at_box
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/mystery_box/on_hover [ at @n[tag=bs.interaction.target] ]
#

execute if entity @n[tag=mgs.mb_display,distance=..3,scores={mgs.mb.anim=1..}] run return run function mgs:v5.1.0/zombies/mystery_box/hud_spinning
# Ready: name the weapon waiting to be collected (read its item_name; fall back to a generic prompt)
data remove storage mgs:temp _mb_hover_name
execute if entity @n[tag=mgs.mb_display,distance=..3] run data modify storage mgs:temp _mb_hover_name set from entity @n[tag=mgs.mb_display,distance=..3] item.components."minecraft:item_name"
execute if entity @n[tag=mgs.mb_display,distance=..3] if data storage mgs:temp _mb_hover_name run return run function mgs:v5.1.0/zombies/mystery_box/hud_ready_named
execute if entity @n[tag=mgs.mb_display,distance=..3] run return run function mgs:v5.1.0/zombies/mystery_box/hud_ready
function mgs:v5.1.0/zombies/mystery_box/hud_price

