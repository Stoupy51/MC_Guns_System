
#> mgs:v5.1.0/multiplayer/gamemodes/demo/pick_sides
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/setup
#

# Per site, which team owns the nearest spawn.
scoreboard players set #demo_near_red mgs.data 0
scoreboard players set #demo_near_blue mgs.data 0
execute as @e[tag=mgs.demo_obj] at @s run function mgs:v5.1.0/multiplayer/gamemodes/demo/tally_site

# The side that lost the tally attacks; a tie keeps Red attacking (CoD default).
scoreboard players set #demo_attackers mgs.data 1
execute if score #demo_near_red mgs.data > #demo_near_blue mgs.data run scoreboard players set #demo_attackers mgs.data 2

