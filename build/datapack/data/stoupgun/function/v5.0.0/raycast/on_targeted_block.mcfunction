
#> stoupgun:v5.0.0/raycast/on_targeted_block
#
# @within	stoupgun:v5.0.0/right_click/handle
#

# Allow bullets to pierce 2 blocks at most
execute if score $raycast.piercing bs.lambda matches 1..3 run scoreboard players remove $raycast.piercing bs.lambda 1
execute if score $raycast.piercing bs.lambda matches 5.. run scoreboard players set $raycast.piercing bs.lambda 3

# Divide damage per 2
execute store result storage stoupgun:gun stats.damage float 0.5 run data get storage stoupgun:gun stats.damage

execute if block ~ ~ ~ #stoupgun:v5.0.0/sounds/glass run playsound minecraft:block.glass.break block @a ~ ~ ~ 1
execute if block ~ ~ ~ #stoupgun:v5.0.0/sounds/water run playsound minecraft:ambient.underwater.exit block @a ~ ~ ~ 0.25 1.5
execute if block ~ ~ ~ #stoupgun:v5.0.0/sounds/cloth run playsound stoupgun:common.cloth_bullet_impact block @a ~ ~ ~ 1
execute if block ~ ~ ~ #stoupgun:v5.0.0/sounds/dirt run playsound stoupgun:common.dirt_bullet_impact block @a ~ ~ ~ 1
execute if block ~ ~ ~ #stoupgun:v5.0.0/sounds/mud run playsound stoupgun:common.mud_bullet_impact block @a ~ ~ ~ 1
execute if block ~ ~ ~ #stoupgun:v5.0.0/sounds/wood run playsound stoupgun:common.wood_bullet_impact block @a ~ ~ ~ 1

