
#> mgs:v5.4.1/kicks/type_4_ds
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/kicks/apply_ds
#

execute if score @s mgs.kick_dir matches 1 run rotate @s ~-0.0975 ~-1.3
execute if score @s mgs.kick_dir matches 2 run rotate @s ~-0.039 ~-1.3
execute if score @s mgs.kick_dir matches 3 run rotate @s ~-0.0 ~-1.3
execute if score @s mgs.kick_dir matches 4 run rotate @s ~0.039 ~-1.3
execute if score @s mgs.kick_dir matches 5 run rotate @s ~0.0975 ~-1.3

