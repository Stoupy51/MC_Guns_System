
#> mgs:v5.0.0/raycast/check_headshot
#
# @within	mgs:v5.0.0/raycast/on_targeted_entity
#

scoreboard players set #is_headshot mgs.data 0
execute store result score #entity_y mgs.data run data get entity @s Pos[1] 1000
execute store result score #hit_y mgs.data run data get storage bs:lambda raycast.hit_point[1] 1000
scoreboard players operation #y_diff mgs.data = #hit_y mgs.data
scoreboard players operation #y_diff mgs.data -= #entity_y mgs.data
execute if score #y_diff mgs.data matches 1200.. run scoreboard players set #is_headshot mgs.data 1
execute unless score #is_headshot mgs.data matches 1 run scoreboard players operation #damage mgs.data /= #2 mgs.data

