
#> mgs:v5.3.0/kicks/type_0
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/kicks/apply
#

execute if score @s mgs.kick_dir matches 1 run rotate @s ~-0.05 ~-0.25
execute if score @s mgs.kick_dir matches 2 run rotate @s ~-0.025 ~-0.25
execute if score @s mgs.kick_dir matches 3 run rotate @s ~-0.0 ~-0.25
execute if score @s mgs.kick_dir matches 4 run rotate @s ~0.025 ~-0.25
execute if score @s mgs.kick_dir matches 5 run rotate @s ~0.05 ~-0.25

