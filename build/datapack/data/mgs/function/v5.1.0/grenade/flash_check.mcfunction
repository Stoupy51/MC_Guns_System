
#> mgs:v5.1.0/grenade/flash_check
#
# @executed	at @s
#
# @within	mgs:v5.1.0/grenade/flash_area
#

# Run as the player, at them; the grenade carries mgs.flash_source.

# Within 3 blocks: always flashed.
execute if entity @e[tag=mgs.flash_source,distance=..3] run return run function mgs:v5.1.0/grenade/flash_player

# Within a 110 degree view cone.
execute at @n[tag=mgs.flash_source] store result score #in_fov mgs.data run function #bs.view:in_view_ata {angle:110}
execute unless score #in_fov mgs.data matches 1 run return 0

scoreboard players set #can_see mgs.data 0
execute at @n[tag=mgs.flash_source] store result score #can_see mgs.data run function #bs.view:can_see_ata {with:{}}
execute unless score #can_see mgs.data matches 1 run return 0

function mgs:v5.1.0/grenade/flash_player

