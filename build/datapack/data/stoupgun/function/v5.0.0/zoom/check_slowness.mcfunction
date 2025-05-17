
#> stoupgun:v5.0.0/zoom/check_slowness
#
# @within	stoupgun:v5.0.0/zoom/main
#

# If player was zooming and switched slot so no longer holding a gun, remove slowness effect
execute unless score @s stoupgun.zoom matches 1 run return fail
playsound stoupgun:common/lean_out player @s ~ ~1000000 ~ 1000000
scoreboard players reset @s stoupgun.zoom
effect clear @s slowness

# TODO optionnal: Find the weapon in inventory and turn it back to non-zoom model

