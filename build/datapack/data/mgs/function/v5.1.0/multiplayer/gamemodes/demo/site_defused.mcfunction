
#> mgs:v5.1.0/multiplayer/gamemodes/demo/site_defused
#
# @executed	as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/site_defuse_tick
#

tag @a remove mgs.xp_earner
execute if score @s mgs.demo_owner matches 1 run tag @a[scores={mgs.mp.team=2},predicate=mgs:v5.1.0/is_sneaking,gamemode=!spectator,distance=..3.0] add mgs.xp_earner
execute if score @s mgs.demo_owner matches 2 run tag @a[scores={mgs.mp.team=1},predicate=mgs:v5.1.0/is_sneaking,gamemode=!spectator,distance=..3.0] add mgs.xp_earner
execute as @a[tag=mgs.xp_earner] run function mgs:v5.1.0/progression/mp/award_bomb_defuse

scoreboard players set @s mgs.demo_state 0
scoreboard players set @s mgs.demo_prog 0
scoreboard players set @s mgs.demo_fuse 0
scoreboard players set @s mgs.demo_owner 0
kill @e[tag=mgs.demo_bomb,distance=..2]
kill @e[tag=mgs.demo_bomb_vis,distance=..2]
kill @e[tag=mgs.demo_bomb_hud,distance=..2]

execute if entity @s[tag=mgs.demo_site_A] run tellraw @a[tag=!mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_defused_at_a","color":"aqua","bold":true}]
execute if entity @s[tag=mgs.demo_site_A] run tellraw @a[tag=mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_defused_at_a","color":"aqua","bold":true},[" ",{"text":"+25 XP","color":"gold"}]]
execute if entity @s[tag=mgs.demo_site_B] run tellraw @a[tag=!mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_defused_at_b","color":"aqua","bold":true}]
execute if entity @s[tag=mgs.demo_site_B] run tellraw @a[tag=mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_defused_at_b","color":"aqua","bold":true},[" ",{"text":"+25 XP","color":"gold"}]]
execute if entity @s[tag=mgs.demo_site_C] run tellraw @a[tag=!mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_defused_at_c","color":"aqua","bold":true}]
execute if entity @s[tag=mgs.demo_site_C] run tellraw @a[tag=mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_defused_at_c","color":"aqua","bold":true},[" ",{"text":"+25 XP","color":"gold"}]]
execute if entity @s[tag=mgs.demo_site_D] run tellraw @a[tag=!mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_defused_at_d","color":"aqua","bold":true}]
execute if entity @s[tag=mgs.demo_site_D] run tellraw @a[tag=mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_defused_at_d","color":"aqua","bold":true},[" ",{"text":"+25 XP","color":"gold"}]]
tag @a remove mgs.xp_earner
playsound minecraft:block.note_block.bit player @a ~ ~ ~ 1 1.5

