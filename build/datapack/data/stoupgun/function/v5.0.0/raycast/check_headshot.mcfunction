
#> stoupgun:v5.0.0/raycast/check_headshot
#
# @within	stoupgun:v5.0.0/raycast/on_targeted_entity
#

scoreboard players set #is_headshot stoupgun.data 0
execute store result score #entity_y stoupgun.data run data get entity @s Pos[1] 1000
execute store result score #hit_y stoupgun.data run data get storage bs:lambda raycast.hit_point[1] 1000
scoreboard players operation #y_diff stoupgun.data = #hit_y stoupgun.data
scoreboard players operation #y_diff stoupgun.data -= #entity_y stoupgun.data
execute if score #y_diff stoupgun.data matches 1200.. run scoreboard players set #is_headshot stoupgun.data 1
execute unless score #is_headshot stoupgun.data matches 1 run scoreboard players operation #damage stoupgun.data /= #2 stoupgun.data

