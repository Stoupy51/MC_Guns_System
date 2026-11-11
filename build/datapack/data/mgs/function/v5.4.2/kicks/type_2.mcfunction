
#> mgs:v5.4.2/kicks/type_2
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/kicks/apply
#

execute if score @s mgs.kick_dir matches 1 run rotate @s ~-0.11 ~-1.0
execute if score @s mgs.kick_dir matches 2 run rotate @s ~-0.05 ~-1.0
execute if score @s mgs.kick_dir matches 3 run rotate @s ~-0.0 ~-1.0
execute if score @s mgs.kick_dir matches 4 run rotate @s ~0.05 ~-1.0
execute if score @s mgs.kick_dir matches 5 run rotate @s ~0.11 ~-1.0

