
#> mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_planted
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/try_plant
#

scoreboard players set #snd_bomb_state mgs.data 2
scoreboard players set #snd_bomb_timer mgs.data 900
scoreboard players set #snd_plant_progress mgs.data 0

# Force the countdown label to be written on the very next tick
scoreboard players set #snd_bomb_sec_shown mgs.data -1

# The marker is the logic anchor (defuse range, explosion origin) and is invisible, which is why planting
# used to change nothing on screen. The block_display is the bomb players actually see and the text
# display carries the countdown, so both sides can read the state of the round from across the room.
summon minecraft:marker ~ ~ ~ {Tags:["mgs.snd_bomb","mgs.gm_entity"]}
summon minecraft:block_display ~ ~ ~ {Tags:["mgs.snd_bomb_vis","mgs.gm_entity"],block_state:{Name:"minecraft:tnt"},transformation:{translation:[-0.25f,0.0f,-0.25f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[0.5f,0.5f,0.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}}
summon minecraft:text_display ~ ~ ~ {Tags:["mgs.snd_bomb_hud","mgs.gm_entity"],billboard:"vertical",text:[[{"text":"💣 ","color":"red","bold":true}, {"translate":"mgs.planted"}]],transformation:{translation:[0.0f,1.1f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]},shadow:true,see_through:true}

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_planted","color":"red","bold":true}]
playsound minecraft:block.note_block.pling player @a ~ ~ ~ 1 0.5

