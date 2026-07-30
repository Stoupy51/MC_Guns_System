
#> mgs:v5.1.0/multiplayer/gamemodes/snd/place_planted_bomb
#
# @executed	as @e[tag=mgs.snd_obj,limit=1,sort=nearest] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_planted [ as @e[tag=mgs.snd_obj,limit=1,sort=nearest] & at @s ]
#

summon minecraft:marker ~ ~ ~ {Tags:["mgs.snd_bomb","mgs.gm_entity"]}
summon minecraft:block_display ~ ~ ~ {Tags:["mgs.snd_bomb_vis","mgs.gm_entity"],block_state:{Name:"minecraft:tnt"},transformation:{translation:[-0.25f,0.0f,-0.25f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[0.5f,0.5f,0.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}}
summon minecraft:text_display ~ ~ ~ {Tags:["mgs.snd_bomb_hud","mgs.gm_entity"],billboard:"vertical",text:[[{"text":"💣 ","color":"red","bold":true}, {"translate":"mgs.planted"}]],transformation:{translation:[0.0f,1.1f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]},shadow:true,see_through:true}

# Name the site so the defenders know which one to rotate to
execute if entity @s[tag=mgs.snd_site_A] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_planted_at_a","color":"red","bold":true}]
execute if entity @s[tag=mgs.snd_site_B] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_planted_at_b","color":"red","bold":true}]
execute if entity @s[tag=mgs.snd_site_C] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_planted_at_c","color":"red","bold":true}]
execute if entity @s[tag=mgs.snd_site_D] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_planted_at_d","color":"red","bold":true}]

