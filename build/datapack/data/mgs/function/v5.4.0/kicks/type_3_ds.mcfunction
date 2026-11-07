
#> mgs:v5.4.0/kicks/type_3_ds
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/kicks/apply_ds
#

execute if score @s mgs.kick_dir matches 1 run rotate @s ~-0.0845 ~-0.975
execute if score @s mgs.kick_dir matches 2 run rotate @s ~-0.039 ~-0.975
execute if score @s mgs.kick_dir matches 3 run rotate @s ~-0.0 ~-0.975
execute if score @s mgs.kick_dir matches 4 run rotate @s ~0.039 ~-0.975
execute if score @s mgs.kick_dir matches 5 run rotate @s ~0.0845 ~-0.975

