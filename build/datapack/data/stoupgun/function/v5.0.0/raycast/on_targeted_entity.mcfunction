
#> stoupgun:v5.0.0/raycast/on_targeted_entity
#
# @within	stoupgun:v5.0.0/right_click/handle
#

particle happy_villager ~ ~ ~ 0 0 0 0 10

execute if block ~ ~ ~ #stoupgun:v5.0.0/sounds/glass run playsound minecraft:block.glass.break block @a ~ ~ ~ 1
execute if block ~ ~ ~ #stoupgun:v5.0.0/sounds/water run playsound minecraft:ambient.underwater.exit block @a ~ ~ ~ 0.25 1.5
execute if block ~ ~ ~ #stoupgun:v5.0.0/sounds/cloth run playsound stoupgun:common.cloth_bullet_impact block @a ~ ~ ~ 1
execute if block ~ ~ ~ #stoupgun:v5.0.0/sounds/dirt run playsound stoupgun:common.dirt_bullet_impact block @a ~ ~ ~ 1
execute if block ~ ~ ~ #stoupgun:v5.0.0/sounds/mud run playsound stoupgun:common.mud_bullet_impact block @a ~ ~ ~ 1
execute if block ~ ~ ~ #stoupgun:v5.0.0/sounds/wood run playsound stoupgun:common.wood_bullet_impact block @a ~ ~ ~ 1

