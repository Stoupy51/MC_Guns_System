
#> mgs:v5.1.0/zombies/perks/dying_wish_end
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/perks/dying_wish_tick
#

attribute @s minecraft:attack_damage modifier remove mgs:dying_wish
effect clear @s minecraft:resistance
effect clear @s minecraft:fire_resistance
effect clear @s minecraft:strength
effect clear @s minecraft:speed
tag @s remove mgs.dying_wish_active
scoreboard players set @s mgs.zb.dw_timer 0

# Left at 1 HP (BO behaviour). /data can't write a player's Health and the max-health clamp trick
# doesn't reliably pull current HP down (both attribute sets collapse in one tick), so deal an exact
# (Health - 1) hit with generic_kill — it bypasses armor, resistance and effects, landing the player
# on precisely 1 HP. Health*1000 for sub-HP precision; skip if already at/below 1.
execute store result score #dw_hp mgs.data run data get entity @s Health 1000
scoreboard players remove #dw_hp mgs.data 1000
execute if score #dw_hp mgs.data matches 1.. run function mgs:v5.1.0/zombies/perks/dying_wish_to_1
title @s times 3 25 10
title @s subtitle [[{"text":"...","color":"gray"}, {"translate":"mgs.barely_alive"}]]

