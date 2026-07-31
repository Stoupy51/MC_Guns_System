
#> mgs:v5.1.0/multiplayer/gamemodes/demo/pick_sides
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/setup
#

# Tally, per bomb site, which team owns the spawn point closest to it.
scoreboard players set #demo_near_red mgs.data 0
scoreboard players set #demo_near_blue mgs.data 0
execute as @e[tag=mgs.demo_obj] at @s run function mgs:v5.1.0/multiplayer/gamemodes/demo/tally_site

# Attackers are whichever side did NOT win that tally. A tie keeps Red attacking, the CoD default.
scoreboard players set #demo_attackers mgs.data 1
execute if score #demo_near_red mgs.data > #demo_near_blue mgs.data run scoreboard players set #demo_attackers mgs.data 2

