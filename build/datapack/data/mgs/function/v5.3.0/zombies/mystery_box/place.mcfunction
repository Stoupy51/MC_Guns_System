
#> mgs:v5.3.0/zombies/mystery_box/place
#
# @executed	as @n[tag=mgs.mb_new] & at @s
#
# @within	mgs:v5.3.0/zombies/mystery_box/setup_pos_iter [ as @n[tag=mgs.mb_new] & at @s ]
#

execute if score @s mgs.mb.roll matches 0 run execute positioned ~ ~0.5 ~ positioned ^ ^0.6 ^0.3 run tp @s ~ ~0.9 ~
execute if score @s mgs.mb.roll matches 1 run execute positioned ~ ~0.5 ~ positioned ^-0.6 ^ ^0.3 run tp @s ~ ~0.9 ~
execute if score @s mgs.mb.roll matches 2 run execute positioned ~ ~0.5 ~ positioned ^ ^-0.6 ^0.3 run tp @s ~ ~0.9 ~
execute if score @s mgs.mb.roll matches 3 run execute positioned ~ ~0.5 ~ positioned ^0.6 ^ ^0.3 run tp @s ~ ~0.9 ~

