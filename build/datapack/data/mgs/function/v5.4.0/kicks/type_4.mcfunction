
#> mgs:v5.4.0/kicks/type_4
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/kicks/apply
#

execute if score @s mgs.kick_dir matches 1 run rotate @s ~-0.15 ~-2.0
execute if score @s mgs.kick_dir matches 2 run rotate @s ~-0.06 ~-2.0
execute if score @s mgs.kick_dir matches 3 run rotate @s ~-0.0 ~-2.0
execute if score @s mgs.kick_dir matches 4 run rotate @s ~0.06 ~-2.0
execute if score @s mgs.kick_dir matches 5 run rotate @s ~0.15 ~-2.0

