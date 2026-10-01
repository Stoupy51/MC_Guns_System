
#> mgs:v5.1.0/player/stamina_bar
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/stamina_tick
#

effect clear @s minecraft:saturation
effect clear @s minecraft:hunger

# Read from the auto-updated `food` criterion, no NBT read. Below target: +1 food this tick, never at or above, so the invisible
# saturation (+2 per tick) cannot stack past what is shown; the pulse may leave some, hence the flag.
execute if score @s mgs.food < #stam_t mgs.data run scoreboard players set @s mgs.stam_dirty 1
execute if score @s mgs.food < #stam_t mgs.data run return run effect give @s minecraft:saturation 1 0 true

# Above target: a hunger pulse drains the bar slowly.
execute if score @s mgs.food > #stam_t mgs.data run return run effect give @s minecraft:hunger 1 255 true

# At target and flagged: read saturation and burn leftovers off with hunger pulses, so the next drain shows at once; once 0 the flag clears and the steady state reads no NBT.
execute unless score @s mgs.stam_dirty matches 1 run return 0
execute store result score #stam_sat mgs.data run data get entity @s foodSaturationLevel
execute if score #stam_sat mgs.data matches 1.. run return run effect give @s minecraft:hunger 1 255 true
scoreboard players set @s mgs.stam_dirty 0

