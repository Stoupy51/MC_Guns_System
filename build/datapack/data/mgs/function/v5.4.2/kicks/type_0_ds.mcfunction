
#> mgs:v5.4.2/kicks/type_0_ds
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/kicks/apply_ds
#

execute if score @s mgs.kick_dir matches 1 run rotate @s ~-0.0325 ~-0.1625
execute if score @s mgs.kick_dir matches 2 run rotate @s ~-0.0163 ~-0.1625
execute if score @s mgs.kick_dir matches 3 run rotate @s ~-0.0 ~-0.1625
execute if score @s mgs.kick_dir matches 4 run rotate @s ~0.0163 ~-0.1625
execute if score @s mgs.kick_dir matches 5 run rotate @s ~0.0325 ~-0.1625

