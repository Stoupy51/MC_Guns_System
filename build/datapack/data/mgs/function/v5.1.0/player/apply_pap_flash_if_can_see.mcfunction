
#> mgs:v5.1.0/player/apply_pap_flash_if_can_see
#
# @executed	at @s & anchored eyes & positioned ^ ^ ^0.001 & as @a[distance=..16]
#
# @within	mgs:v5.1.0/player/fire_weapon [ at @s & anchored eyes & positioned ^ ^ ^0.001 & as @a[distance=..16] ]
#

# At most one burst per 2 ticks for this observer
execute if score @s mgs.last_muzzle_flash > #total_tick mgs.data run return 0
scoreboard players set @s mgs.last_muzzle_flash 2
scoreboard players operation @s mgs.last_muzzle_flash += #total_tick mgs.data

# Check line of sight to the muzzle and set #can_see accordingly (score 0 or 1).
scoreboard players set #can_see mgs.data 0
execute if entity @s[tag=mgs.ticking] run scoreboard players set #can_see mgs.data 1
execute if score #can_see mgs.data matches 0 store result score #can_see mgs.data run function #bs.view:can_see_ata {with:{}}
execute if score #can_see mgs.data matches 0 run return 0

# Swap the previous burst for the other slot, so the new one is always a fresh chain.
# The sprite sits at the muzzle, which moves on ADS, so the variant follows this observer's own aim.
function mgs:v5.1.0/player/flash_clear
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
scoreboard players set @s mgs.flash_off 2
scoreboard players operation @s mgs.flash_off += #total_tick mgs.data

