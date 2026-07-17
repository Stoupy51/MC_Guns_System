
#> mgs:v5.1.0/player/stamina_bar
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/stamina_tick
#

effect clear @s minecraft:saturation
effect clear @s minecraft:hunger

# The bar is read from the auto-updated 'food' criterion — no player-NBT read on this path.
# Below target → refill pulse (+1 food this tick). Never given at/above target so the invisible
# saturation side effect (+2/tick) can't stack past what's visible (stamina.md). The pulse may
# leave invisible saturation behind, so flag it for the at-target burn-off below.
execute if score @s mgs.food < #stam_t mgs.data run scoreboard players set @s mgs.stam_dirty 1
execute if score @s mgs.food < #stam_t mgs.data run return run effect give @s minecraft:saturation 1 0 true

# Above target → hunger pulse slowly drains the bar, showing the player they sprint too much
execute if score @s mgs.food > #stam_t mgs.data run return run effect give @s minecraft:hunger 1 255 true

# At target: only while flagged dirty, pay the saturation NBT read and burn leftovers off with
# hunger pulses so the next drain shows immediately; once it reads 0 the flag clears and the
# steady state costs no NBT read at all
execute unless score @s mgs.stam_dirty matches 1 run return 0
execute store result score #stam_sat mgs.data run data get entity @s foodSaturationLevel
execute if score #stam_sat mgs.data matches 1.. run return run effect give @s minecraft:hunger 1 255 true
scoreboard players set @s mgs.stam_dirty 0

