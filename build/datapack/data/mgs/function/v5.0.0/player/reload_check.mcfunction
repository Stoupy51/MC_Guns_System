
#> mgs:v5.0.0/player/reload_check
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# If mainhand is empty and offhand has a weapon, move it to mainhand and reload
execute unless items entity @s weapon.mainhand * if items entity @s weapon.offhand *[custom_data~{mgs:{gun:true}}] run function mgs:v5.0.0/player/swap_and_reload

