
#> mgs:v5.4.0/zombies/near_within_32
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/tag_zombies_near_32 [ as @e[type=minecraft:marker,tag=mgs.zb_cand] ]
#			mgs:v5.4.0/zombies/tag_special_near_32 [ as @e[type=minecraft:marker,tag=mgs.zb_cand] ]
#

execute store result score #zb_dx mgs.data run data get entity @s Pos[0] 10
execute store result score #zb_dy mgs.data run data get entity @s Pos[1] 10
execute store result score #zb_dz mgs.data run data get entity @s Pos[2] 10
scoreboard players operation #zb_dx mgs.data -= #zb_px mgs.data
scoreboard players operation #zb_dy mgs.data -= #zb_py mgs.data
scoreboard players operation #zb_dz mgs.data -= #zb_pz mgs.data
scoreboard players operation #zb_dx mgs.data *= #zb_dx mgs.data
scoreboard players operation #zb_dy mgs.data *= #zb_dy mgs.data
scoreboard players operation #zb_dz mgs.data *= #zb_dz mgs.data
scoreboard players set #zb_nine mgs.data 9
scoreboard players operation #zb_dy mgs.data *= #zb_nine mgs.data
scoreboard players operation #zb_dx mgs.data += #zb_dz mgs.data
scoreboard players operation #zb_dx mgs.data += #zb_dy mgs.data
execute if score #zb_dx mgs.data matches ..102400 run tag @s add mgs.zb_near

execute store result score #zb_dx mgs.data run data get entity @s Pos[0] 10
execute store result score #zb_dy mgs.data run data get entity @s Pos[1] 10
execute store result score #zb_dz mgs.data run data get entity @s Pos[2] 10
scoreboard players operation #zb_dx mgs.data -= #zb_px mgs.data
scoreboard players operation #zb_dy mgs.data -= #zb_py mgs.data
scoreboard players operation #zb_dz mgs.data -= #zb_pz mgs.data
scoreboard players operation #zb_dx mgs.data *= #zb_dx mgs.data
scoreboard players operation #zb_dy mgs.data *= #zb_dy mgs.data
scoreboard players operation #zb_dz mgs.data *= #zb_dz mgs.data
scoreboard players set #zb_nine mgs.data 9
scoreboard players operation #zb_dy mgs.data *= #zb_nine mgs.data
scoreboard players operation #zb_dx mgs.data += #zb_dz mgs.data
scoreboard players operation #zb_dx mgs.data += #zb_dy mgs.data
execute if score #zb_dx mgs.data matches ..102400 run tag @s add mgs.zb_near

