
#> mgs:v5.0.0/multiplayer/editor/append_mag_consumable
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/append_mag_slots
#

# Total bullets = mag_bullets (capacity) * pmag_count (user's chosen count)
execute store result score #mag_bullets mgs.data run data get storage mgs:temp _mag_bullets
scoreboard players operation #mag_bullets mgs.data *= #pmag_count mgs.data
execute store result storage mgs:temp _mag_bullets int 1 run scoreboard players get #mag_bullets mgs.data
execute store result storage mgs:temp _inv_n int 1 run scoreboard players get #inv_slot mgs.data
function mgs:v5.0.0/multiplayer/editor/append_mag_consumable_macro with storage mgs:temp
scoreboard players add #inv_slot mgs.data 1

