
#> mgs:v5.1.0/player/apply_flash_if_can_see
#
# @executed	at @s & anchored eyes & positioned ^ ^ ^0.001 & as @a[distance=..16]
#
# @within	mgs:v5.1.0/player/fire_weapon [ at @s & anchored eyes & positioned ^ ^ ^0.001 & as @a[distance=..16] ]
#

# The clock only re-arms when the id has been absent for a tick, so refuse to re-apply too early
execute if score @s mgs.last_muzzle_flash > #total_tick mgs.data run return 0
scoreboard players set @s mgs.last_muzzle_flash 3
scoreboard players operation @s mgs.last_muzzle_flash += #total_tick mgs.data

# Check line of sight to the muzzle and set #can_see accordingly (score 0 or 1).
scoreboard players set #can_see mgs.data 0
execute if entity @s[tag=mgs.ticking] run scoreboard players set #can_see mgs.data 1
execute if score #can_see mgs.data matches 0 store result score #can_see mgs.data run function #bs.view:can_see_ata {with:{}}
execute if score #can_see mgs.data matches 0 run return 0

# The sprite sits at the muzzle, which moves on ADS, so the id depends on this observer's own aim
execute if score @s mgs.zoom matches 1 run posteffect add @s mgs:flash_zoom
execute if score @s mgs.zoom matches 1 run scoreboard players set @s mgs.flash_id 1
execute unless score @s mgs.zoom matches 1 run posteffect add @s mgs:flash
execute unless score @s mgs.zoom matches 1 run scoreboard players set @s mgs.flash_id 3
scoreboard players set @s mgs.flash_off 2

