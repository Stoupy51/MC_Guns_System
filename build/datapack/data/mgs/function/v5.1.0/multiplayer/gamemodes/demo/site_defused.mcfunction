
#> mgs:v5.1.0/multiplayer/gamemodes/demo/site_defused
#
# @executed	as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/site_defuse_tick
#

scoreboard players set @s mgs.demo_state 0
scoreboard players set @s mgs.demo_prog 0
scoreboard players set @s mgs.demo_fuse 0
scoreboard players set @s mgs.demo_owner 0
kill @e[tag=mgs.demo_bomb,distance=..2]
kill @e[tag=mgs.demo_bomb_vis,distance=..2]
kill @e[tag=mgs.demo_bomb_hud,distance=..2]

execute if entity @s[tag=mgs.demo_site_A] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_defused_at_a","color":"aqua","bold":true}]
execute if entity @s[tag=mgs.demo_site_B] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_defused_at_b","color":"aqua","bold":true}]
execute if entity @s[tag=mgs.demo_site_C] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_defused_at_c","color":"aqua","bold":true}]
execute if entity @s[tag=mgs.demo_site_D] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_defused_at_d","color":"aqua","bold":true}]
execute unless entity @s[tag=mgs.demo_site_A] unless entity @s[tag=mgs.demo_site_B] unless entity @s[tag=mgs.demo_site_C] unless entity @s[tag=mgs.demo_site_D] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_defused","color":"aqua","bold":true}]
playsound minecraft:block.note_block.bit player @a ~ ~ ~ 1 1.5

