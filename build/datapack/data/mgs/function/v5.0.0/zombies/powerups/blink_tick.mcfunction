
#> mgs:v5.0.0/zombies/powerups/blink_tick
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.0/zombies/powerups/entity_tick
#

# Toggle visibility every ~5 ticks using global blink state (managed in game_tick)
execute if score #zb_blink_state mgs.data matches 0 run data merge entity @s {view_range:0.0f}
execute if score #zb_blink_state mgs.data matches 1 run data merge entity @s {view_range:64.0f}
execute if score #zb_blink_state mgs.data matches 0 as @e[tag=mgs.pu_text,distance=..3] run data merge entity @s {view_range:0.0f}
execute if score #zb_blink_state mgs.data matches 1 as @e[tag=mgs.pu_text,distance=..3] run data merge entity @s {view_range:64.0f}

