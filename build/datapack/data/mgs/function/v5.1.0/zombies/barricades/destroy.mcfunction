
#> mgs:v5.1.0/zombies/barricades/destroy
#
# @executed	positioned ^ ^ ^-1
#
# @within	mgs:v5.1.0/zombies/barricades/handle_removing
#

# @s = intact barricade display → transitions to destroyed
scoreboard players set @s mgs.zb.barricade.state 1
scoreboard players set @s mgs.zb.barricade.r_timer 0

# Clean up removing zombie
execute as @e[tag=mgs.barricade_removing] if score @s mgs.zb.barricade.removing_id = #barricade_id mgs.data run tag @s remove mgs.barricade_removing

# Switch to disabled block state
data modify entity @s block_state set from entity @s data.block_disabled

# Sound + particles
particle minecraft:large_smoke ~ ~0.5 ~ 0.4 0.4 0.4 0.02 6
particle minecraft:crit ~ ~0.5 ~ 0.4 0.4 0.4 0.05 8
playsound minecraft:entity.zombie.break_wooden_door block @a[distance=..32] ~ ~ ~ 1.0 1.0

