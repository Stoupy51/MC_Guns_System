
#> mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_planted
#
# @executed	as @a[tag=mgs.snd_carrier,limit=1] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/tick [ as @a[tag=mgs.snd_carrier,limit=1] & at @s ]
#

scoreboard players set #snd_bomb_state mgs.data 2
scoreboard players set #snd_bomb_timer mgs.data 900
scoreboard players set #snd_plant_progress mgs.data 0

# The countdown label is written on the next tick.
scoreboard players set #snd_bomb_sec_shown mgs.data -1

tag @s remove mgs.snd_carrier
kill @e[tag=mgs.snd_carrier_label]

# Marked so the site announce in place_planted_bomb carries their XP.
function mgs:v5.1.0/progression/mp/award_bomb_plant
tag @a remove mgs.xp_earner
tag @s add mgs.xp_earner

# On the site, not at the player's feet: a CoD bomb sits at the site, so both teams know where the defuse happens.
execute as @e[tag=mgs.snd_obj,limit=1,sort=nearest] at @s run function mgs:v5.1.0/multiplayer/gamemodes/snd/place_planted_bomb
tag @a remove mgs.xp_earner

playsound minecraft:block.note_block.pling player @a ~ ~ ~ 1 0.5

