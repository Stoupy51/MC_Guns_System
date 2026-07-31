
#> mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_planted
#
# @executed	as @a[tag=mgs.snd_carrier,limit=1] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/tick [ as @a[tag=mgs.snd_carrier,limit=1] & at @s ]
#

scoreboard players set #snd_bomb_state mgs.data 2
scoreboard players set #snd_bomb_timer mgs.data 900
scoreboard players set #snd_plant_progress mgs.data 0

# Force the countdown label to be written on the very next tick
scoreboard players set #snd_bomb_sec_shown mgs.data -1

# The bomb leaves the carrier's hands
tag @s remove mgs.snd_carrier
kill @e[tag=mgs.snd_carrier_label]

# Plant it ON the site, not wherever the player happened to be standing. A CoD bomb sits at the site, so
# both teams know exactly where the defuse happens; planting at the player's feet is the Counter-Strike
# "anywhere inside the zone" rule and made the bomb hard to find.
execute as @e[tag=mgs.snd_obj,limit=1,sort=nearest] at @s run function mgs:v5.1.0/multiplayer/gamemodes/snd/place_planted_bomb

playsound minecraft:block.note_block.pling player @a ~ ~ ~ 1 0.5

