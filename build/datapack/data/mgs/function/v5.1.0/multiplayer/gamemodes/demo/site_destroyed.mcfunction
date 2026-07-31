
#> mgs:v5.1.0/multiplayer/gamemodes/demo/site_destroyed
#
# @executed	as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/site_fuse_tick
#

scoreboard players set @s mgs.demo_state 2
scoreboard players set @s mgs.demo_prog 0
scoreboard players operation #demo_last_owner mgs.data = @s mgs.demo_owner

particle minecraft:explosion_emitter ~ ~1 ~ 2 2 2 0 5
playsound minecraft:entity.generic.explode player @a ~ ~ ~ 2 0.8
execute as @a[distance=..8.0,gamemode=!creative,gamemode=!spectator,scores={mgs.mp.in_game=1..}] run data modify storage mgs:input with set value {}
execute as @a[distance=..8.0,gamemode=!creative,gamemode=!spectator,scores={mgs.mp.in_game=1..}] run function mgs:v5.1.0/multiplayer/simulate_death

# The site is wrecked: no chest to plant on, rubble and a struck-out label in its place
kill @e[tag=mgs.demo_bomb,distance=..2]
kill @e[tag=mgs.demo_bomb_vis,distance=..2]
kill @e[tag=mgs.demo_bomb_hud,distance=..2]
setblock ~ ~ ~ air
summon minecraft:block_display ~ ~ ~ {Tags:["mgs.demo_rubble","mgs.gm_entity"],block_state:{Name:"minecraft:polished_blackstone"},transformation:{translation:[-0.3f,0.0f,-0.3f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[0.6f,0.2f,0.6f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}}
summon minecraft:text_display ~ ~ ~ {Tags:["mgs.demo_wreck","mgs.gm_entity"],billboard:"vertical",text:[[{"text":"💥 ","color":"dark_gray"}, {"translate":"mgs.destroyed"}]],transformation:{translation:[0.0f,1.4f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]},shadow:true,see_through:true}

execute if entity @s[tag=mgs.demo_site_A] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_site_a_destroyed","color":"red","bold":true}]
execute if entity @s[tag=mgs.demo_site_B] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_site_b_destroyed","color":"red","bold":true}]
execute if entity @s[tag=mgs.demo_site_C] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_site_c_destroyed","color":"red","bold":true}]
execute if entity @s[tag=mgs.demo_site_D] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_site_d_destroyed","color":"red","bold":true}]
execute unless entity @s[tag=mgs.demo_site_A] unless entity @s[tag=mgs.demo_site_B] unless entity @s[tag=mgs.demo_site_C] unless entity @s[tag=mgs.demo_site_D] run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💣 ",{"translate":"mgs.bomb_site_destroyed","color":"red","bold":true}]

# Destroying a site buys time to reach the other one
scoreboard players add #demo_timer mgs.data 1200
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"⏱ ",[{"text":"+60","color":"gold"}, {"translate":"mgs.s_on_the_clock"}]]

# Overtime is a single neutral site, so blowing it up takes the MATCH for whoever planted it
execute if score #demo_round mgs.data matches 3.. run return run function mgs:v5.1.0/multiplayer/gamemodes/demo/overtime_won

# Otherwise the attackers only win once nothing is left standing
execute unless entity @e[tag=mgs.demo_obj,scores={mgs.demo_state=..1}] run function mgs:v5.1.0/multiplayer/gamemodes/demo/attackers_win

