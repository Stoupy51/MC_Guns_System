
#> mgs:v5.0.0/missions/normalize_bounds
#
# @within	mgs:v5.0.0/missions/start
#

execute if score #bound_x1 mgs.data > #bound_x2 mgs.data run scoreboard players operation #swap mgs.data = #bound_x1 mgs.data
execute if score #bound_x1 mgs.data > #bound_x2 mgs.data run scoreboard players operation #bound_x1 mgs.data = #bound_x2 mgs.data
execute if score #swap mgs.data matches -2147483648.. run scoreboard players operation #bound_x2 mgs.data = #swap mgs.data
execute if score #swap mgs.data matches -2147483648.. run scoreboard players reset #swap mgs.data

execute if score #bound_y1 mgs.data > #bound_y2 mgs.data run scoreboard players operation #swap mgs.data = #bound_y1 mgs.data
execute if score #bound_y1 mgs.data > #bound_y2 mgs.data run scoreboard players operation #bound_y1 mgs.data = #bound_y2 mgs.data
execute if score #swap mgs.data matches -2147483648.. run scoreboard players operation #bound_y2 mgs.data = #swap mgs.data
execute if score #swap mgs.data matches -2147483648.. run scoreboard players reset #swap mgs.data

execute if score #bound_z1 mgs.data > #bound_z2 mgs.data run scoreboard players operation #swap mgs.data = #bound_z1 mgs.data
execute if score #bound_z1 mgs.data > #bound_z2 mgs.data run scoreboard players operation #bound_z1 mgs.data = #bound_z2 mgs.data
execute if score #swap mgs.data matches -2147483648.. run scoreboard players operation #bound_z2 mgs.data = #swap mgs.data
execute if score #swap mgs.data matches -2147483648.. run scoreboard players reset #swap mgs.data

