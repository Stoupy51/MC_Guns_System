
#> mgs:v5.1.0/multiplayer/gamemodes/snd/pick_sides
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/setup
#

# Tally, per bomb site, which team owns the spawn point closest to it.
scoreboard players set #snd_near_red mgs.data 0
scoreboard players set #snd_near_blue mgs.data 0
execute as @e[tag=mgs.snd_obj] at @s run function mgs:v5.1.0/multiplayer/gamemodes/snd/tally_site

# Attackers are whichever side did NOT win that tally. A tie keeps Red attacking, the CoD default.
scoreboard players set #snd_attackers mgs.data 1
execute if score #snd_near_red mgs.data > #snd_near_blue mgs.data run scoreboard players set #snd_attackers mgs.data 2

