
#> mgs:v5.0.1/player/stamina_bar
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/stamina_tick
#

effect clear @s minecraft:saturation
effect clear @s minecraft:hunger
execute store result score #stam_food mgs.data run data get entity @s foodLevel
execute store result score #stam_sat mgs.data run data get entity @s foodSaturationLevel

# Below target → refill pulse (+1 food this tick). Never given at/above target so the invisible
# saturation side effect (+2/tick) can't stack past what's visible (stamina.md).
execute if score #stam_food mgs.data < #stam_t mgs.data run effect give @s minecraft:saturation 1 0 true

# Above target → hunger pulse slowly drains the bar, showing the player they sprint too much
execute if score #stam_food mgs.data > #stam_t mgs.data run effect give @s minecraft:hunger 1 255 true

# At target with leftover invisible saturation → burn it off so the next drain shows immediately
execute if score #stam_food mgs.data = #stam_t mgs.data if score #stam_sat mgs.data matches 1.. run effect give @s minecraft:hunger 1 255 true

