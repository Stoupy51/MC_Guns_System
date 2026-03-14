
#> mgs:v5.0.0/multiplayer/gamemodes/snd/bomb_planted
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/snd/try_plant
#

scoreboard players set #snd_bomb_state mgs.data 2
scoreboard players set #snd_bomb_timer mgs.data 900

# Summon bomb entity at planter's position
summon minecraft:marker ~ ~ ~ {Tags:["mgs.snd_bomb","mgs.gm_entity"]}

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],[{"text":"💣 ","color":"red","bold":true}, {"translate":"mgs.bomb_planted"}]]
playsound minecraft:block.note_block.pling player @a ~ ~ ~ 1 0.5

