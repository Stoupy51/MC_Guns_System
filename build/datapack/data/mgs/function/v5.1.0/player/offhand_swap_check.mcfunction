
#> mgs:v5.1.0/player/offhand_swap_check
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

# Main hand empty and a gun in the offhand.
execute unless items entity @s weapon.mainhand * if items entity @s weapon.offhand *[custom_data~{mgs:{gun:true}}] run function mgs:v5.1.0/player/swap_and_reload

