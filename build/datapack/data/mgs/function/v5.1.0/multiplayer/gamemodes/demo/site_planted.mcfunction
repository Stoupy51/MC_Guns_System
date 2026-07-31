
#> mgs:v5.1.0/multiplayer/gamemodes/demo/site_planted
#
# @executed	as @e[tag=mgs.demo_obj,scores={mgs.demo_state=0}] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/site_plant_tick
#

scoreboard players set @s mgs.demo_state 1
scoreboard players set @s mgs.demo_fuse 200
scoreboard players set @s mgs.demo_prog 0

summon minecraft:marker ~ ~ ~ {Tags:["mgs.demo_bomb","mgs.gm_entity"]}
summon minecraft:block_display ~ ~ ~ {Tags:["mgs.demo_bomb_vis","mgs.gm_entity"],block_state:{Name:"minecraft:tnt"},transformation:{translation:[-0.25f,0.625f,-0.25f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[0.5f,0.5f,0.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}}
summon minecraft:text_display ~ ~ ~ {Tags:["mgs.demo_bomb_hud","mgs.gm_entity"],billboard:"vertical",text:[[{"text":"💣 ","color":"red","bold":true}, {"translate":"mgs.planted"}]],transformation:{translation:[0.0f,1.4f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]},shadow:true,see_through:true}

execute if entity @s[tag=mgs.demo_site_A] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_planted_at_a","color":"red","bold":true}]
execute if entity @s[tag=mgs.demo_site_B] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_planted_at_b","color":"red","bold":true}]
execute if entity @s[tag=mgs.demo_site_C] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_planted_at_c","color":"red","bold":true}]
execute if entity @s[tag=mgs.demo_site_D] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_planted_at_d","color":"red","bold":true}]
execute unless entity @s[tag=mgs.demo_site_A] unless entity @s[tag=mgs.demo_site_B] unless entity @s[tag=mgs.demo_site_C] unless entity @s[tag=mgs.demo_site_D] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_planted","color":"red","bold":true}]
playsound minecraft:block.note_block.pling player @a ~ ~ ~ 1 0.5

