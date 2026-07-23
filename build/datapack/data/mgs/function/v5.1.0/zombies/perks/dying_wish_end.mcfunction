
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

# Left at 1 HP (BO behaviour). /data can't write a player's Health, so briefly clamp max health to
# 1 (which pulls current HP down to 1), then restore the real max — a max-health increase never
# refills, so the player stays at 1 HP.
attribute @s minecraft:max_health base set 1
execute if score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20
title @s times 3 25 10
title @s subtitle [[{"text":"...","color":"gray"}, {"translate":"mgs.barely_alive"}]]

