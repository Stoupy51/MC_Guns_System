
#> mgs:v5.0.1/zombies/powerups/blink_tick
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.1/zombies/powerups/entity_tick
#

# "Off" frame: dim item_display to black, hide text_display
execute if score #zb_blink_state mgs.data matches 0 run data merge entity @s {brightness:{block:0,sky:0}}
# "On" frame: restore item_display to full brightness
execute if score #zb_blink_state mgs.data matches 1 run data merge entity @s {brightness:{block:15,sky:15}}
# text_display has no brightness tag — use view_range toggle instead
execute if score #zb_blink_state mgs.data matches 0 as @n[tag=mgs.pu_text,distance=..3] run data merge entity @s {view_range:0.0f}
execute if score #zb_blink_state mgs.data matches 1 as @n[tag=mgs.pu_text,distance=..3] run data merge entity @s {view_range:64.0f}

