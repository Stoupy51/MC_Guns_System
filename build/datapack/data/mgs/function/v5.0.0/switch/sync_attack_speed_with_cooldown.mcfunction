
#> mgs:v5.0.0/switch/sync_attack_speed_with_cooldown
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/switch/force_switch_animation
#

## Formula: [attack_speed = (20.0 / cooldown) - 4.0] <- where 4.0 is default attack speed
# Compute attack speed based of @s mgs.cooldown (with 3 digits precision)
scoreboard players set #attack_speed mgs.data 20000
scoreboard players operation #attack_speed mgs.data /= @s mgs.cooldown
scoreboard players remove #attack_speed mgs.data 4000

# Summon a temporary entity that will be used to modify the attack speed attribute modifier from the player's mainhand slot
tag @s add mgs.to_modify
execute summon item_display run function mgs:v5.0.0/switch/modify_attack_speed
tag @s remove mgs.to_modify

