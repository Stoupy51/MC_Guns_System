
#> mgs:v5.3.0/player/apply_pap_flash
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/player/fire_weapon
#

# At most one burst per 2 ticks
execute if score @s mgs.last_muzzle_flash > #total_tick mgs.data run return 0
scoreboard players set @s mgs.last_muzzle_flash 2
scoreboard players operation @s mgs.last_muzzle_flash += #total_tick mgs.data

# Swap the previous burst for the other slot, so the new one is always a fresh chain.
# The sprite sits at the muzzle, which moves on ADS, so the variant follows the shooter's aim.
function mgs:v5.3.0/player/flash_clear
execute store success score #flash_slot_was_1 mgs.data if score @s mgs.flash_slot matches 1
execute store result score @s mgs.flash_slot if score #flash_slot_was_1 mgs.data matches 0
execute unless score @s mgs.zoom matches 1 if score @s mgs.flash_slot matches 0 run posteffect add @s mgs:flash_pap_0
execute unless score @s mgs.zoom matches 1 if score @s mgs.flash_slot matches 0 run scoreboard players set @s mgs.flash_id 5
execute unless score @s mgs.zoom matches 1 if score @s mgs.flash_slot matches 1 run posteffect add @s mgs:flash_pap_1
execute unless score @s mgs.zoom matches 1 if score @s mgs.flash_slot matches 1 run scoreboard players set @s mgs.flash_id 6
execute if score @s mgs.zoom matches 1 if score @s mgs.flash_slot matches 0 run posteffect add @s mgs:flash_pap_zoom_0
execute if score @s mgs.zoom matches 1 if score @s mgs.flash_slot matches 0 run scoreboard players set @s mgs.flash_id 7
execute if score @s mgs.zoom matches 1 if score @s mgs.flash_slot matches 1 run posteffect add @s mgs:flash_pap_zoom_1
execute if score @s mgs.zoom matches 1 if score @s mgs.flash_slot matches 1 run scoreboard players set @s mgs.flash_id 8

# The flash lights from unmagnified depth, so the zoom must run after it; the crosshair stays on top
function mgs:v5.3.0/zoom/fx_to_back
function mgs:v5.3.0/zoom/crosshair_to_back
scoreboard players set @s mgs.flash_off 2
scoreboard players operation @s mgs.flash_off += #total_tick mgs.data

