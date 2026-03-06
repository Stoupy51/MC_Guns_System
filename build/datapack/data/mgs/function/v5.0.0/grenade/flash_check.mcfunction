
#> mgs:v5.0.0/grenade/flash_check
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.0.0/grenade/flash_area
#

# @s = player, position = player's position (from at @s)
# Flash source grenade is tagged mgs.flash_source

# Close range override: within 3 blocks, always flash (too close to avoid)
execute if entity @e[tag=mgs.flash_source,distance=..3] run return run function mgs:v5.0.0/grenade/flash_player

# Direction check: is the grenade within the player's field of view? (110 degree cone)
execute at @n[tag=mgs.flash_source] store result score #in_fov mgs.data run function #bs.view:in_view_ata {angle:110}
execute unless score #in_fov mgs.data matches 1 run return 0

# Line-of-sight check: can the player see the grenade? (no blocks between)
scoreboard players set #can_see mgs.data 0
execute at @n[tag=mgs.flash_source] store result score #can_see mgs.data run function #bs.view:can_see_ata {with:{}}
execute unless score #can_see mgs.data matches 1 run return 0

# Both checks passed: flash the player
function mgs:v5.0.0/grenade/flash_player

