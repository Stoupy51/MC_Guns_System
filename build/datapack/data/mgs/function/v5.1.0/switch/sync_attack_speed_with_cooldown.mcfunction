
#> mgs:v5.1.0/switch/sync_attack_speed_with_cooldown
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/switch/force_switch_animation
#

## attack_speed = 20.0 / cooldown - 4.0 (4.0 is the default), with 3 digits of precision.
scoreboard players operation #remaining_cooldown mgs.data = @s mgs.cooldown
scoreboard players operation #remaining_cooldown mgs.data -= #total_tick mgs.data
scoreboard players set #attack_speed mgs.data 20000
scoreboard players operation #attack_speed mgs.data /= #remaining_cooldown mgs.data
scoreboard players remove #attack_speed mgs.data 4000

# A temporary item_display edits the attribute modifier of the mainhand item.
tag @s add mgs.to_modify
execute summon item_display run function mgs:v5.1.0/switch/modify_attack_speed
tag @s remove mgs.to_modify

